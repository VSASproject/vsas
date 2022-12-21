#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef enum {
    NALU_TYPE_SLICE = 1,
    NALU_TYPE_DPA = 2,
    NALU_TYPE_DPB = 3,
    NALU_TYPE_DPC = 4,
    NALU_TYPE_IDR = 5,
    NALU_TYPE_SEI = 6,
    NALU_TYPE_SPS = 7,
    NALU_TYPE_PPS = 8,
    NALU_TYPE_AUD = 9,
    NALU_TYPE_EOSEQ = 10,
    NALU_TYPE_EOSTREAM = 11,
    NALU_TYPE_FILL = 12,
} NaluType;

typedef enum {
    NALU_PRIORITY_DISPOSABLE = 0,
    NALU_PRIRITY_LOW = 1,
    NALU_PRIORITY_HIGH = 2,
    NALU_PRIORITY_HIGHEST = 3
} NaluPriority;


typedef struct
{
    int startcodeprefix_len;      //! 4 for parameter sets and first slice in picture, 3 for everything else (suggested)
    unsigned len;                 //! Length of the NAL unit (Excluding the start code, which does not belong to the NALU)
    unsigned max_size;            //! Nal Unit Buffer size
    int forbidden_bit;            //! should be always FALSE
    int nal_reference_idc;        //! NALU_PRIORITY_xxxx
    int nal_unit_type;            //! NALU_TYPE_xxxx    
    char* buf;                    //! contains the first byte followed by the EBSP
} NALU_t;

FILE* h264bitstream = NULL;                //!< the bit stream file

int info2 = 0, info3 = 0;

static int FindStartCode2(unsigned char* Buf) {
    if (Buf[0] != 0 || Buf[1] != 0 || Buf[2] != 1) return 0; //0x000001?
    else return 1;
}

static int FindStartCode3(unsigned char* Buf) {
    if (Buf[0] != 0 || Buf[1] != 0 || Buf[2] != 0 || Buf[3] != 1) return 0;//0x00000001?
    else return 1;
}


int GetAnnexbNALU(NALU_t* nalu) {
    int pos = 0;
    int StartCodeFound, rewind;
    unsigned char* Buf;

    if ((Buf = (unsigned char*)calloc(nalu->max_size, sizeof(char))) == NULL)
        printf("GetAnnexbNALU: Could not allocate Buf memory\n");

    nalu->startcodeprefix_len = 3;

    if (3 != fread(Buf, 1, 3, h264bitstream)) {
        free(Buf);
        return 0;
    }
    info2 = FindStartCode2(Buf);
    if (info2 != 1) {
        if (1 != fread(Buf + 3, 1, 1, h264bitstream)) {
            free(Buf);
            return 0;
        }
        info3 = FindStartCode3(Buf);
        if (info3 != 1) {
            free(Buf);
            return -1;
        }
        else {
            pos = 4;
            nalu->startcodeprefix_len = 4;
        }
    }
    else {
        nalu->startcodeprefix_len = 3;
        pos = 3;
    }
    StartCodeFound = 0;
    info2 = 0;
    info3 = 0;

    while (!StartCodeFound) {
        if (feof(h264bitstream)) {
            nalu->len = (pos - 1) - nalu->startcodeprefix_len;
            memcpy(nalu->buf, &Buf[nalu->startcodeprefix_len], nalu->len);
            nalu->forbidden_bit = nalu->buf[0] & 0x80; //1 bit
            nalu->nal_reference_idc = nalu->buf[0] & 0x60; // 2 bit
            nalu->nal_unit_type = (nalu->buf[0]) & 0x1f;// 5 bit
            free(Buf);
            return pos - 1;
        }
        Buf[pos++] = fgetc(h264bitstream);
        info3 = FindStartCode3(&Buf[pos - 4]);
        if (info3 != 1)
            info2 = FindStartCode2(&Buf[pos - 3]);
        StartCodeFound = (info2 == 1 || info3 == 1);
    }

    // Here, we have found another start code (and read length of startcode bytes more than we should
    // have.  Hence, go back in the file
    rewind = (info3 == 1) ? -4 : -3;

    if (0 != fseek(h264bitstream, rewind, SEEK_CUR)) {
        free(Buf);
        printf("GetAnnexbNALU: Cannot fseek in the bit stream file");
    }

    // Here the Start code, the complete NALU, and the next start code is in the Buf.  
    // The size of Buf is pos, pos+rewind are the number of bytes excluding the next
    // start code, and (pos+rewind)-startcodeprefix_len is the size of the NALU excluding the start code

    nalu->len = (pos + rewind) - nalu->startcodeprefix_len;
    memcpy(nalu->buf, &Buf[nalu->startcodeprefix_len], nalu->len);//
    nalu->forbidden_bit = nalu->buf[0] & 0x80; //1 bit
    nalu->nal_reference_idc = nalu->buf[0] & 0x60; // 2 bit
    nalu->nal_unit_type = (nalu->buf[0]) & 0x1f;// 5 bit
    free(Buf);

    return (pos + rewind);
}

/*
* cut the bitstream into small ones,
* where i fragments are relialbe
* p fragments are unrelialbe
*/
int file_cut(char *url, char *path_output,int nal_num, int data_offset, int len, char* idc_str) {
    char dispos = 0;
    //if the idc_str is disposible or low priority, means it is not essential
    //then we label it with p prefix on the fragment file
    if (strcmp(idc_str,"DISPOS")==0) {
        dispos = 'p';
    }
    else {
        dispos = 'i';
    }
    char filename[100];
    //construct the filename of fragment
    sprintf(filename, "%c_%d.nal", dispos, nal_num);
    char file_path[200] = "";
    strcpy_s(file_path, path_output);
    strcat_s(file_path, filename);
    //printf("%s", filename);
    FILE* fp;
    fp = fopen(file_path, "wb");
    FILE* h264bitstream = fopen(url, "rb+");
    if (h264bitstream == NULL) {
        printf("Open file error\n");
        return 0;
    }
    fseek(h264bitstream, data_offset, SEEK_SET);
    unsigned char* Buf;

    if ((Buf = (unsigned char*)calloc(10000000, sizeof(char))) == NULL)
        printf("FileCutter: Could not allocate Buf memory\n");
    int read_len = fread(Buf, sizeof(char), len, h264bitstream);
    if (len != read_len) {
        printf("read failed.%d", read_len);
        free(Buf);
        return 0;
    }

    fwrite(Buf, sizeof(char),len, fp);
    fclose(h264bitstream);
    fclose(fp);
    free(Buf);
    return 0;
}

/**
 * Analysis H.264 Bitstream
 * @param url    Location of input H.264 bitstream file.
 */
int simplest_h264_parser(char* url, char* path2, char* path_output) {

    NALU_t* n;
    int buffersize = 100000;

    //FILE *myout=fopen("output_log.txt","wb+");
    FILE* myout = stdout;

    h264bitstream = fopen(url, "rb+");
    if (h264bitstream == NULL) {
        printf("Open file error\n");
        return 0;
    }

    n = (NALU_t*)calloc(1, sizeof(NALU_t));
    if (n == NULL) {
        printf("Alloc NALU Error\n");
        return 0;
    }

    n->max_size = buffersize;
    n->buf = (char*)calloc(buffersize, sizeof(char));
    if (n->buf == NULL) {
        free(n);
        printf("AllocNALU: n->buf");
        return 0;
    }

    int data_offset = 0;
    int nal_num = 0;
    int start_byte = 0;
    printf("-----+-------- NALU Table ------+---------+\n");
    printf(" NUM |    POS  |    IDC |  TYPE |   LEN   |\n");
    printf("-----+---------+--------+-------+---------+\n");

    while (!feof(h264bitstream))
    {
        int data_lenth;
        data_lenth = GetAnnexbNALU(n);

        char type_str[20] = { 0 };
        switch (n->nal_unit_type) {
        case NALU_TYPE_SLICE:sprintf(type_str, "SLICE"); break;
        case NALU_TYPE_DPA:sprintf(type_str, "DPA"); break;
        case NALU_TYPE_DPB:sprintf(type_str, "DPB"); break;
        case NALU_TYPE_DPC:sprintf(type_str, "DPC"); break;
        case NALU_TYPE_IDR:sprintf(type_str, "IDR"); break;
        case NALU_TYPE_SEI:sprintf(type_str, "SEI"); break;
        case NALU_TYPE_SPS:sprintf(type_str, "SPS"); break;
        case NALU_TYPE_PPS:sprintf(type_str, "PPS"); break;
        case NALU_TYPE_AUD:sprintf(type_str, "AUD"); break;
        case NALU_TYPE_EOSEQ:sprintf(type_str, "EOSEQ"); break;
        case NALU_TYPE_EOSTREAM:sprintf(type_str, "EOSTREAM"); break;
        case NALU_TYPE_FILL:sprintf(type_str, "FILL"); break;
        }
        char idc_str[20] = { 0 };
        switch (n->nal_reference_idc >> 5) {
        case NALU_PRIORITY_DISPOSABLE:sprintf(idc_str, "DISPOS"); break;
        case NALU_PRIRITY_LOW:sprintf(idc_str, "LOW"); break;
        case NALU_PRIORITY_HIGH:sprintf(idc_str, "HIGH"); break;
        case NALU_PRIORITY_HIGHEST:sprintf(idc_str, "HIGHEST"); break;
        }

        fprintf(myout, "%5d| %8d| %7s| %6s| %8d|\n", nal_num, data_offset, idc_str, type_str, n->len);
        //printf("%d %d %d %s\n", nal_num, data_offset, n->len + 4, idc_str);
        //file_cut(path2, nal_num, data_offset, n->len + n->startcodeprefix_len, idc_str);
        file_cut(path2, path_output, nal_num, data_offset, data_lenth, idc_str);
        data_offset = data_offset + data_lenth;

        nal_num++;
    }

    //Free
    if (n) {
        if (n->buf) {
            free(n->buf);
            n->buf = NULL;
        }
        free(n);
    }
    return 0;
}
int main(int argc, char *argv[]) {
    //char path[105] = "C:\\Users\\walter\\Dropbox\\Research Projects\\MetaverseQUIC\\vpcc_eng\\sample_attr_h264\\s2_GOF0_attribute.h264";
    //char path2[107] = "C:\\Users\\walter\\Dropbox\\Research Projects\\MetaverseQUIC\\vpcc_eng\\sample_attr_h264\\s2_GOF0_attribute.h264.2";
    //char path[105] = "C:\\Users\\walter\\Dropbox\\Research Projects\\MetaverseQUIC\\vpcc_eng\\sample_full_h264\\s2.h264";
    //char path2[107] = "C:\\Users\\walter\\Dropbox\\Research Projects\\MetaverseQUIC\\vpcc_eng\\sample_full_h264\\s2.h264.2";
    //char path[105] = "C:\\Users\\walter\\Dropbox\\Research Projects\\MetaverseQUIC\\vpcc_eng\\exp1_attr_h264\\s2_GOF0_attribute.h264";
    //char path2[107] = "C:\\Users\\walter\\Dropbox\\Research Projects\\MetaverseQUIC\\vpcc_eng\\exp1_attr_h264\\s2_GOF0_attribute.h264.2";
    //char path[105] = "C:\\Users\\walter\\Dropbox\\Research Projects\\MetaverseQUIC\\vpcc_eng\\exp2_attr_h264\\s2_GOF0_geometry.h264";
    //char path2[107] = "C:\\Users\\walter\\Dropbox\\Research Projects\\MetaverseQUIC\\vpcc_eng\\exp2_attr_h264\\s2_GOF0_geometry.h264.2";
    //char path[105] = "C:\\Users\\walter\\PycharmProjects\\nalDropPSNR\\data\\origin\\attribute\\s2_GOF0_attribute.h264";
    //char path2[107] = "C:\\Users\\walter\\PycharmProjects\\nalDropPSNR\\data\\origin\\attribute\\s2_GOF0_attribute.h264.2";
    //char path[105] = "C:\\Users\\walter\\PycharmProjects\\nalDropPSNR\\data\\origin\\geometry\\s2_GOF0_geometry.h264";
    //char path2[107] = "C:\\Users\\walter\\PycharmProjects\\nalDropPSNR\\data\\origin\\geometry\\s2_GOF0_geometry.h264.2";
    //char path[105] = "C:\\Users\\walter\\PycharmProjects\\nalDropPSNR\\data\\origin\\occupancy\\s2_GOF0_occupancy.h264";
    //char path2[107] = "C:\\Users\\walter\\PycharmProjects\\nalDropPSNR\\data\\origin\\occupancy\\s2_GOF0_occupancy.h264.2";
    char path[105] = "D:\\loot_vox10.h264";
    char suffix[10] = ".2";
    char path2[107] = "D:\\loot_vox10.h264.2";
    char path_output[200] = "";
    printf("%d\n", argc);
    if (argc == 3) {
        strcpy_s(path, 100, argv[1]);
        strcpy_s(path2, 100, path);
        strcat_s(path2, suffix);
        strcpy_s(path_output, 100, argv[2]);
        printf("%s %s %s\n", path, path2, path_output);
    }
    
    int output = simplest_h264_parser(path, path2, path_output);
    printf("%d\n", output);
    return 0;
}
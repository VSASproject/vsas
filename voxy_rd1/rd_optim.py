#This moduel is used to do the Rate-Distortion optimization
#given the model from rd_fit module, where the coefficienct
#will be stored in a csv, so that rd_optim can run directly
#without compute the model parameters from scratch.
#This part is called offline on the server-side to prepare for the ABR
#It needs to be called each time a new video is uploaded and needed to
#be encoded through MPEG V-PCC's PccEncoder tool


import cvxpy as cvx
from rd_fit_mod import aqp_br_model,aqp_psnr_model,gqp_psnr_model,gqp_br_model

#find the best qp that maximize the PSNR while
#below the bandwidth limits bw.
def rd_problem(bw):
    #quantization paramter
    qp = cvx.Variable()
    #downsampling rate
    dr = cvx.Variable()

    # objective
    obj = cvx.Minimize(qp)

    #constraints
    cts = [qp>=1, qp<=25, aqp_br_model(qp) <= bw]

    prob = cvx.Problem(obj, cts)
    prob.solve()

    print(aqp_psnr_model(qp.value))
    print(qp.value, dr.value)
    #return qp.value, dr.value

if __name__=="__main__":
    #demo()
    rd_problem(30000)

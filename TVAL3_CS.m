function y = TVAL3_CS(imgs,b,dx,dy,mu,beta,iters,tol,cnt,TVnorm,nneg,TVL2)

clear opts

if nneg==1
  opts.nonneg = true;
end

if nneg==2
  opts.nonneg = false;
end

if TVL2==1
  opts.TVL2= true;
end
if TVL2 == 2
  opts.TVL2 = false;
end


%% Run TVAL3

opts.mu = mu;
opts.beta = beta;
opts.tol = tol;
opts.maxit = iters;
opts.maxcnt = cnt;
opts.TVnorm = TVnorm;
#opts.scale_A = false;
#opts.scale_b=false;

[y, out] = TVAL3(imgs,b',dx,dy,opts);
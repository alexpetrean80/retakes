pkg load statistics;

% a
#xpdf=0:3;
%print("a\n");
%ypdf = binopdf(xpdf, 3, 1/2)
%plot(xpdf, ypdf, "+");
#hold on

%b
#xcdf = 0:0.1:3;
%print("b\n");
%ycdf = binocdf(xcdf, 3, 1/2)
%plot(xcdf, ycdf, "*-");
#hold off

% c
printf("c\n");
pc1 = binopdf(0, 3, 1/2)
pc2 = 1 - binopdf(1, 3, 1/2)

% d
printf("d\n");
pd1 = binocdf(2, 3, 1/2)
pd2 = binocdf(1, 3, 1/2)

% e
printf("e\n");
pe1 = 1 - binocdf(0, 3, 1/2)
pe2 = 1 - binocdf(1, 3, 1/2)

% f
printf("f\n");
n = 10000000;
% 1 - heads; 0 - tails
C = sum(rand(3, n) < 0.5);
hist(C);




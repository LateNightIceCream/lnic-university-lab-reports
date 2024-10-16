Data <- read.csv("komm-benchmark2/output.csv", sep = ",", dec = ".")
Data$n <- Data$n / 1000
regmodel <- lm(time_us ~ n, data = Data)

intercept <- regmodel$coefficients[1]
rise <- regmodel$coefficients[2]
subtitle <- sprintf("RTT = %.3f µs/kB * n + %.3f µs", rise, intercept)

pdf("regression.pdf", 10.0, 6.18)

plot(Data$n, Data$time_us,
          main="Bytes vs RTT",
          xlab="Echo Bytes / kB",
          ylab="RTT / µs",
          sub=subtitle)
abline(regmodel, col="red")



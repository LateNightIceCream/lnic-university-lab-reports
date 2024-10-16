Data1 <- read.csv("last_trajectory.csv", sep = ",", dec = ".")

subtitle <- ""

pdf("plot.pdf", 10.0, 6.18)

plot(Data1$t, Data1$x2,
          main="Mass-Spring-Damper Trajectory",
          xlab="t / s",
          ylab="x / m",
          sub=subtitle)

#abline(regmodel, col="red")


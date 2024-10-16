Data1 <- read.csv("speeds.csv", sep = ",", dec = ".")

Data1$cores <- as.numeric(Data1$cores)
Data1$time_ms <- as.numeric(Data1$time_ms)

num_runs <- 2000000
sequential_time_ms <- 12290

speedups <- (Data1$time_ms / Data1$time_ms[1])^(-1)

subtitle <- ""


pdf("plot_amdahl_duration.pdf", 10.0, 6.18)

plot(Data1$cores, Data1$time_ms,
          main="Mass-Spring-Damper Speedup Benchmark",
          xlab="number of cores",
          ylab="duration / ms",
          sub=subtitle)


eq = function(x){x}
curve(eq, from=1, to=8, add=TRUE, col="red", lty=2)


pdf("plot_amdahl_speedup.pdf", 10.0, 6.18)

plot(Data1$cores, speedups,
          main="Mass-Spring-Damper Speedup Benchmark",
          xlab="number of cores",
          ylab="speedup",
          ylim=c(1, 8),
          sub=subtitle)


eq = function(x){x}
curve(eq, from=1, to=8, add=TRUE, lty=2)

legend(1, 8, c("measured", "ideal"), lty=c(NA,2), pch=c(1, NA))

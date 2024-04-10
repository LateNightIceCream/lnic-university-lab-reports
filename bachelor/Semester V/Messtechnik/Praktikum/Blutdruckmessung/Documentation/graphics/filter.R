library("signal")
library("ggplot2")

file <- read.csv("raw_data.csv", skip=1, col.names = c("second", "volt"))

time    <- file$second + 5
voltage <- file$volt

offset <- mean(tail(voltage, 84), na.rm=TRUE)

voltage <- voltage-offset

lowerIndex <- 1149
upperIndex <- 1600

cutTime    <- time[lowerIndex:upperIndex]
cutVoltage <- voltage[lowerIndex:upperIndex]

a = 2.669069
b = -0.05132788
exponentialModel <- function(t) {
  a * exp(b * t)
}


flatVoltage <- cutVoltage - exponentialModel(cutTime)

# Filtering
fCutoff     <- 4 #Hz
fSampling   <- 1/( cutTime[2]-cutTime[1] )
fNormalized <- fCutoff / fSampling
fNyquist    <- fNormalized / 2

#fir1(numberOfTaps, [cutoffFrequency(ies)], "filterType")
filterCoefficients  <- fir1(50, fNyquist)
filterCoefficients
flatVoltageFiltered <- filter(filterCoefficients, 1, voltage)


pdf("wab.pdf", width=10, height=6.18)
#qplot(time, flatVoltageFiltered, geom=c("line"))
plot(freqz(filterCoefficients))

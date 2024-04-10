library(ggplot2)

outputName   <- "corr_fft.pdf"
outputWidth  <- 10
outputHeight <- outputWidth * 0.618

data <- read.csv("corr_fft.csv", skip = 0, col.names = c("frequency", "amplitude"));

lowerIndex <- 0
upperIndex <- 150

cutSecond <- data$frequency[lowerIndex:upperIndex]
cutVolt   <- data$amplitude[lowerIndex:upperIndex]

cutData <- data.frame(cutSecond, cutVolt)
colnames(cutData) <- c("frequency", "amplitude")

subtitleString <- sprintf("")

xbreaks <- seq(0,10,2)

plot <- ggplot( cutData, aes(x = frequency, y = amplitude)) +
  geom_segment(aes(frequency,amplitude,xend=frequency,yend=amplitude-amplitude)) + 
  geom_point(aes(frequency,amplitude),size=1.618, color="gray71") +

  scale_x_continuous(breaks = xbreaks) +

  theme_minimal() +
  theme(plot.title = element_text(color = "gray21", size=1.6180339887498948^5), plot.subtitle = element_text(color = "grey80", size=1.6180339887498948^5)) +
  ggtitle("DFT der Autokorrelationsfunktion") +
  labs(subtitle = subtitleString)+
#  stat_function(fun = exponentialModelMilliVolt, color="gray80") +
  #geom_line(size=0.15) +
  ylab("Amplitude") +
  xlab("f / Hz")


pdf(outputName, width = outputWidth, height = outputHeight)
plot

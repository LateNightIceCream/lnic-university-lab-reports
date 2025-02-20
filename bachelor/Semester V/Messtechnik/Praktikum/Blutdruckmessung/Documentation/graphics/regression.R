library(ggplot2)

outputName   <- "regression.pdf"
outputWidth  <- 10
outputHeight <- outputWidth * 0.618

offset <- 0.0033011
data <- read.csv("raw_data.csv", skip = 1, col.names = c("second", "volt"));
data$second <- data$second + 5

lowerIndex <- 1149
upperIndex <- 1600

cutSecond <- data$second[lowerIndex:upperIndex]
cutVolt   <- data$volt[lowerIndex:upperIndex]

cutData <- data.frame(cutSecond, cutVolt)
colnames(cutData) <- c("second", "volt")

limMod <- lm(volt ~ second, data = cutData)
expMod <- lm(log(volt) ~ second, data = cutData)


linearModel <- function (t) {
  (-0.02392 * t + 1.28845)*1000
}

a = exp(summary(expMod)$coefficients[1])
b = summary(expMod)$coefficients[2]
exponentialModel <- function (t) {
  a * exp(b * t)
}

a
b

exponentialModelMilliVolt <- function (t) {
  exponentialModel(t) * 1000
}

newVolt <- cutData$volt - exponentialModel(cutData$second)
newSecond <- cutData$second

newData <- data.frame(newSecond, newVolt)
colnames(newData) <- c("second", "volt")

subtitleString <- sprintf("Modellfunktion u(t) = a * exp(b * t): a = %f V, b = %f s^-1", a, b)

plot <- ggplot( cutData, aes(x = second, y = volt * 1000)) +
  theme_minimal() +
  theme(plot.title = element_text(color = "gray21", size=1.6180339887498948^5), plot.subtitle = element_text(color = "grey80", size=1.6180339887498948^5)) +
  ggtitle("Entnahme der relevanten Daten und exponentielle Regression") +
  labs(subtitle = subtitleString)+
  stat_function(fun = exponentialModelMilliVolt, color="gray80") +
  geom_line(size=0.15) +
  ylab("Spannung / mV") +
  xlab("t / s")


pdf(outputName, width = outputWidth, height = outputHeight)
plot

library(ggplot2)

outputName   <- "raw_data.pdf"
outputWidth  <- 10
outputHeight <- outputWidth * 0.618

data <- read.csv("raw_data.csv", skip = 1, col.names = c("second", "volt"));
data$second <- data$second + 5


plot <- ggplot( data, aes(x = second, y = volt * 1000)) +
  theme_minimal() +
  theme(plot.title = element_text(color = "gray21", size=1.6180339887498948^5), plot.subtitle = element_text(color = "grey80", size=1.6180339887498948^5)) +
  ggtitle("Rohe Daten der Spannungsmessung") +
  labs(subtitle = "Daten des Oszilloskops bei Messung am Ausgang des Instrumentenverstärkers") +
  geom_line(size=0.15) +
  ylab("Spannung / mV") +
  xlab("t / s")


pdf(outputName, width = outputWidth, height = outputHeight)
plot

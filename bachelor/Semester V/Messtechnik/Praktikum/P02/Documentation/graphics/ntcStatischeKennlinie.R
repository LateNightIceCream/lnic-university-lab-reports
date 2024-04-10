library(ggplot2)

outputName   <- "ntcStatischeKennlinie.pdf"
outputWidth  <- 10
outputHeight <- outputWidth * 0.618

A = -15.5322
B = 5229.973
C = -160451
D = -5.414091 * 10^6
R25 = 33 # kOhm

RT <- function (T) {
  R25 * exp(A + B/(T+273) + C/((T+273)^2) + D/((T+273)^3))
}

plot <- ggplot( data.frame(x=c(-10, 110)), aes(x)) +
  theme_minimal() +
  theme(plot.title = element_text(color = "gray21", size=1.6180339887498948^5), plot.subtitle = element_text(color = "grey80", size=1.6180339887498948^5)) +
  ggtitle("Statische NTC-Kennlinie") +
  labs(subtitle = "Vishay NTCLE100E3, R25 = 33 kOhm") +
  stat_function(fun = RT, color="#282828") +
  scale_x_continuous(breaks=seq(-10,110,20)) +
  ylab(bquote("R / k"~Omega)) +
  xlab("T / °C")


pdf(outputName, width = outputWidth, height = outputHeight)
plot

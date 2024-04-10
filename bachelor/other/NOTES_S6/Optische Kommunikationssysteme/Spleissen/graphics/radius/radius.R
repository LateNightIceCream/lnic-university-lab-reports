library(ggplot2)
library(latex2exp)

width    <- 10
height   <- 0.618 * width
pdfName  <- "radius.pdf"

data <- read.csv("radius.csv")

plot <- ggplot(data = data, aes(x=r, y=D)) +
  theme_minimal() +

  theme(plot.title    = element_text(color = "gray21", size=1.6180339887498948^5),
        plot.subtitle = element_text(color = "grey70", size=1.6180339887498948^5)) +

  ggtitle("Relative Empfangsleistung über Verschiebung vom Zentrum") +
  labs(subtitle = "Polynomregression n = 2: y = -0.16574 * x^2 - 0.69513 * x + 0.31448") +

  xlab(TeX('Verschiebung vom Zentrum, $\\Delta r / \\mu m$'))+
  ylab(TeX('$\\frac{P_{empf}}{P_{opt}} / dB$'))+
  geom_point() +
  geom_line()

pdf(pdfName, width, height)
plot

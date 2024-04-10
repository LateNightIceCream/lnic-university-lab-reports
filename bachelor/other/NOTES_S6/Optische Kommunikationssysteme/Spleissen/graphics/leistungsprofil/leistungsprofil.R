library(ggplot2)
library(latex2exp)

width    <- 10
height   <- 0.618 * width
pdfName  <- "leistungsprofil.pdf"
pdfName2 <- "leistungsprofil_linear.pdf"

data <- read.csv("leistungsprofil.csv")

model <- lm(data$delta_opt ~ poly(data$x, 2, raw=TRUE))
summary(model)

a <- -0.16574
b <- -0.69513
c <- 0.31448

bep <- function (x) {
  a * x^2 + b * x + c
}

modenfelddampf <- 1/(exp(2))
modenfeld_db   <- 10 * log10(modenfelddampf)

radius <- function(dampf) {
  (-b - sqrt(b^2 - 4*a*(c-dampf))) / (2 * a)
}
modenfelddampf
modenfeld_db
modenfeldradius = radius(modenfeld_db)
modenfeldradius / 4.5


plot <- ggplot(data = data, aes(x=x, y=delta_opt)) +
  theme_minimal() +

  theme(plot.title    = element_text(color = "gray21", size=1.6180339887498948^5),
        plot.subtitle = element_text(color = "grey70", size=1.6180339887498948^5)) +

  ggtitle("Relative Empfangsleistung über Verschiebung vom Zentrum") +
  labs(subtitle = "Polynomregression n = 2: y = -0.16574 * x^2 - 0.69513 * x + 0.31448") +

  xlab(TeX('Verschiebung vom Zentrum, $\\Delta r / \\mu m$'))+
  ylab(TeX('$\\frac{P_{empf}}{P_{opt}} / dB$'))+
  stat_function(fun = bep, color = "grey80") +
  #stat_smooth(method="lm", se=TRUE, fill=NA, formula=y ~ poly(x, 2, raw=TRUE),colour="red") +
  geom_point() +
  geom_segment(aes(x = modenfeldradius, y = 0, xend = modenfeldradius, yend = modenfeld_db), color = "gray69", linetype = "dashed") +
  geom_segment(aes(x = 0, y = modenfeld_db, xend = modenfeldradius, yend = modenfeld_db), color = "gray69", linetype = "dashed")

pdf(pdfName, width, height)
plot

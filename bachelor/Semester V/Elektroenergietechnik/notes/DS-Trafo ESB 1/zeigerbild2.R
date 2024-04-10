library(ggplot2)

R2strich <- 3.19
X2strich <- 9.74
Z2strich <- complex(real = R2strich, imag = X2strich)

R1 <- 0.077
X2 <- 6.28
Z1 <- complex(real=R1, imag=X2)

XMstrich <- 1413.7

ratio <- 10 / 0.4

U_Zstrich <- 10 * 10^(3) / sqrt(3)

Z <- complex( real = 350 * 10^(-3), imag = 330 * 10^(-3))

#===============================

Zstrich <- Z * (ratio^2)

I2strich <- U_Zstrich / Zstrich

U_Z2 <- I2strich * Z2strich

U_Mstrich <- U_Z2 + U_Zstrich

I1 <- (U_Mstrich / (complex(real = 0, imag = XMstrich))) + I2strich

U_Z1 <- I1 * Z1

U1 <- U_Z1 + U_Mstrich

#===============================

outputName <- "zeigerbild2.pdf"
width      <- 10
height     <- 6.18
                                        
#===============================

complex_arrow <- function (c1, color="black", c2 = complex(real=0, imag=0) ) {

  geom_segment(aes(x = Re(c2), y = Im(c2),
                   xend  = Re(c2) + Re(c1),
                   yend  = Im(c2) + Im(c1)),
               arrow = arrow(length = unit(0.5, "cm")),
               color = color)
}

annotate_arrow <- function (c1, label, c2 = complex(real=0, imag=0)) {

  annotate("text",
           x = Re(c2) + Re(c1) / 2,
           y = Im(c2) + Im(c1) / 2,
           label = label,
           angle =  atan(height/width) * 180/pi )
}

#atan((height * Im(U1))/(width * Re(U1)) ) * 180/pi


plot <- ggplot(data.frame(x=c(0, abs(U1))), aes(x)) +
  theme_minimal() +
#  scale_x_continuous(limits = c(0, abs(U1)) ) +
  coord_polar() +

  geom_segment(aes(y = 0, x= 2, xend = 5, yend = 10))

  ## complex_arrow(U1, "blue") +
  ## annotate_arrow(U1, bquote("U"[1])) +

  ## complex_arrow(U_Zstrich, "green") +
  ## annotate_arrow(U_Zstrich, bquote("U"["Z'"])) +

  ## complex_arrow(U_Mstrich, "gray") +
  ## annotate_arrow(U_Mstrich, bquote("U"["M'"])) +

  ## complex_arrow(U_Z2, "red", U_Zstrich) +
  ## annotate_arrow(U_Z2, bquote("U"["Z2"]), c2 = U_Zstrich) +

  ## complex_arrow(U_Z1, "orange", U_Mstrich) +
  ## annotate_arrow(U_Z1, bquote("U"["Z1"]), c2 = U_Mstrich) 


pdf(outputName, width = width, height = height)
plot

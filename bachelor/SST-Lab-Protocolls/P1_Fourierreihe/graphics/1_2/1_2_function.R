# square wave plot

library(ggplot2)

options(scipen=10000)

epsilon <- 10
tau     <- 4
T1      <- tau * 1.6180339887498948
A      <- 1 #1.381966011

X0     <- 0.618 * A

output_width  <- 10
output_height <- output_width * 0.6180339887498948


ylabel <- bquote( "x" )
xlabel <- bquote( "t" )


xbreaks <- c(0, -tau/2, tau/2, -T1/2, T1/2, -T1, T1)
xlabels <- c(0, bquote("-"~over(tau, 2)), bquote(over(tau, 2)), bquote("-"~over("T", 2)), bquote(over("T", 2)), bquote("-T"), bquote("T"))

#for(n in 1:3) {
  #xbreaks <- c(xbreaks, n*T1)
  #xlabels <- c(xlabels, bquote(.(n)~T))
#}

function_color <- "#00b1db"


####################################################################

p <- ggplot(data.frame(x=c(0,2), y=c(-2,2)), aes(x=x)) +

        theme_minimal() + # maybe theme_bw()
        theme(legend.position="none", plot.title = element_text(color = "gray21", size=1.6180339887498948^5), plot.subtitle = element_text(color = "grey80", size=1.6180339887498948^5)) +
        ggtitle("x(t)") +

        theme(text = element_text(size=16.180339887498948), axis.title.y = element_text(angle = 0, vjust = .5), panel.grid.minor.x = element_blank()) + # rotate axis title

        xlab(xlabel) +
        #ylab(ylabel)  +

        scale_y_continuous(limits=c(-1.618033, 1.6180339887498948), breaks=c(-A,0,A), labels=c("-A", 0, "A")) +
        scale_x_continuous(limits=c(-epsilon, epsilon), breaks=xbreaks, labels=xlabels)
        #scale_x_discrete(limits=1, breaks=c(1,2,3)) #labels=c(0, bquote("-"~over("T1",2)), bquote(over(-tau,2)), bquote(over(-tau,2)), bquote(over(tau,2))) )

delta <- T1

function_color <- "#afafaf"
for (n in -1:1) {

  # solid horizontal lines
  p <- p + geom_segment( x = -tau/2 + n*delta, y = A, xend = tau/2  + n*delta,  yend = A, color=function_color, linetype="solid") +
      geom_segment( x = -T1/2  + n*delta, y = -A, xend = -tau/2 + n*delta,  yend = -A, color=function_color, linetype="solid") +
      geom_segment( x = T1/2   + n*delta, y = -A, xend = tau/2  + n*delta,  yend = -A, color=function_color, linetype="solid")

  # test segment
  #p <- p + geom_segment( x = T1/2, y = 0, xend = T1/2-tau/2 + T1/2, yend = 0, aes(color="blue"), linetype="solid")

  # dashed vertical lines
  p <- p + geom_segment( x = -tau/2 + n*delta, y = -A, xend = -tau/2 + n*delta, yend = A, color=function_color, linetype="dashed")+
           geom_segment( x =  tau/2 + n*delta, y = -A, xend = tau/2 + n*delta,  yend = A, color=function_color, linetype="dashed")
}

function_color <- "#00b1db"
# offset waveform
for (n in -1:1) {



                                        # solid horizontal lines
    p <- p + geom_segment( x = -tau/2 + n*delta, y = A+X0, xend = tau/2  + n*delta,  yend = A+X0, color=function_color, linetype="solid") +
        geom_segment( x = -T1/2  + n*delta, y = -A+X0, xend = -tau/2 + n*delta,  yend = -A+X0, color=function_color, linetype="solid") +
        geom_segment( x = T1/2   + n*delta, y = -A+X0, xend = tau/2  + n*delta,  yend = -A+X0, color=function_color, linetype="solid")

                                        # test segment
                                        #p <- p + geom_segment( x = T1/2, y = 0, xend = T1/2-tau/2 + T1/2, yend = 0, aes(color="blue"), linetype="solid")

                                        # dashed vertical lines
    p <- p + geom_segment( x = -tau/2 + n*delta, y = -A+X0, xend = -tau/2 + n*delta, yend = A+X0, color=function_color, linetype="dashed")+
        geom_segment( x =  tau/2 + n*delta, y = -A+X0, xend = tau/2 + n*delta,  yend = A+X0, color=function_color, linetype="dashed")
}

arrowColor <- "#afafaf"
p <- p + geom_segment ( x = -T/2, y = -A, xend = -T/2, yend = -A + X0, color = arrowColor, linetype = "solid", arrow = arrow())
p <- p + annotate( "text", x = -T/2 + 0.75, y = -A/1.618, label = "X0", color = arrowColor, size = 6.18)


pdf("1_2_function.pdf", width = output_width, height = output_height)
p

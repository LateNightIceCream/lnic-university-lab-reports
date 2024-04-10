library(ggplot2)

csv_data = read.csv("eye_data.csv", header=FALSE)

out_width <- 10
out_height <- 6.18


t = as.numeric(csv_data[1,])
y = as.numeric(csv_data[2,])

data = data.frame(t = t, y = y)

T_SAMPLE = 1.25e-5
T_PERIOD = 2.0e-4

#groups = 1:(length(data$t)/(T_PERIOD/T_SAMPLE))

data$t = data$t %% (T_PERIOD * 2)
data$t

groups = 1:(length(data$t) / 16)
groups

max(data$t)
dat_split = split(data, f = groups)

dat_split$`1`

data$t

p <- ggplot(data = dat_split$`1`, aes(x = t, y = y)) +
#p <- ggplot(data = data, aes(x = t, y = y)) +
  geom_point() +
  geom_line() +
  geom_line(data = dat_split$`2`, aes(x = t, y = y)) +
  geom_line(data = dat_split$`3`, aes(x = t, y = y)) +
  geom_line(data = dat_split$`4`, aes(x = t, y = y))

pdf("output.pdf", out_width, out_height)
p

rm(list = ls())
graphics.off()

library(ggplot2)
library(dplyr)
library(RColorBrewer)
library(wesanderson)

#brewer.pal.info
#display.brewer.all()
#display.brewer.all(type="seq")
#display.brewer.all(type="div")

## Example data
#set.seed(0)
#dat <- data.frame(dates=seq.Date(Sys.Date(), Sys.Date()+99, 1),
#                  value=cumsum(rnorm(100)))

## Determine highlighted regions
#v <- rep(0, 100)
#v[c(5:20, 30:35, 90:100)] <- 1
#
### Get the start and end points for highlighted regions
#inds <- diff(c(0, v))
#start <- dat$dates[inds == 1]
#end <- dat$dates[inds == -1]
#if (length(start) > length(end)) end <- c(end, tail(dat$dates, 1))
#
### highlight region data
#rects <- data.frame(start=start, end=end, group=seq_along(start))
#
#library(ggplot2)
#ggplot(data=dat, aes(dates, value)) +
#  theme_minimal() +
#  geom_line(lty=2, color="steelblue", lwd=1.1) +
#  geom_point() +
#  geom_rect(data=rects, inherit.aes=FALSE, aes(xmin=start, xmax=end, ymin=min(dat$value),
#                ymax=max(dat$value), group=group), color="transparent", fill="orange", alpha=0.3)

#############################################################################################

data_df_vhf_switch <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/adaptive_switch_adaptive_ETS_45_descending/h2_data.csv')
data_df_vhf_switch$type <- 'Adaptive Shaping\n using HTB at Switch\n egress port'

data_df_vhf_meter <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/adaptive_meter_adaptive_ETS_45_descending/h2_data.csv')
data_df_vhf_meter$type <- 'Adaptive Shaping\n using meter table\n of switch'

data_df_vhf <- rbind(data_df_vhf_switch,data_df_vhf_meter)

data_df_uhf_switch <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/adaptive_switch_adaptive_ETS_45_descending/h3_data.csv')
data_df_uhf_switch$type <- 'Adaptive Shaping\n using HTB at Switch\n egress port'

data_df_uhf_meter <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/adaptive_meter_adaptive_ETS_45_descending/h3_data.csv')
data_df_uhf_meter$type <- 'Adaptive Shaping\n using meter table\n of switch'

data_df_uhf <- rbind(data_df_uhf_switch,data_df_uhf_meter)

data_df_satcom <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/adaptive_switch_adaptive_ETS_40_descending/h4_data.csv')
data_df_satcom$Network <- 'SatCom'

data_df_vhf$flow_id <- factor(data_df_vhf$flow_id, levels = c("1", "2", "3", "4", "5"),
                          labels = c("Medical Evacuation", "Obstacle Alert", "Picture", "Chat", "FFT"))

data_df_uhf$flow_id <- factor(data_df_uhf$flow_id, levels = c("6", "7", "8", "9", "10"),
                          labels = c("Medical Evacuation", "Obstacle Alert", "Picture", "Chat", "FFT"))

data_df_satcom$flow_id <- factor(data_df_satcom$flow_id, levels = c("11", "12", "13", "14", "15"),
                          labels = c("Medical Evacuation", "Obstacle Alert", "Picture", "Chat", "FFT"))

#data_df <- rbind(data_df_vhf,data_df_uhf,data_df_satcom)
colnames(data_df_vhf)[which(names(data_df_vhf) == "flow_id")] <- "Messages"
colnames(data_df_uhf)[which(names(data_df_uhf) == "flow_id")] <- "Messages"




gg <- ggplot()
gg <- gg + geom_line(data = data_df_uhf, mapping = aes(x = packet_delay_in_secs, y = packet_seq_no, color=Messages, linetype=Messages))
gg <- gg + geom_point(data = data_df_uhf, mapping = aes(x = packet_delay_in_secs, y = packet_seq_no, color=Messages, shape=Messages), size = 3, stroke=1.3, alpha = 1)
gg <- gg + scale_linetype_manual(values=c("longdash", "twodash", "dashed","dotdash","dotted"))
gg <- gg + scale_shape_manual(values=c(1, 2, 3, 4, 5))
#gg <- gg + scale_color_manual(values=c('#1e2240', '#607dab','#b5c9d5', '#FFE77AFF', '#2C5F2DFF'))
#gg <- gg + scale_color_manual(values=c('#1f1f1f','#660000', '#EA9999', '#E69138', '#B4A7D6'))
gg <- gg + scale_color_manual(values=c('grey40','tomato4', 'tomato', 'goldenrod', '#2C5F2DFF'))
#gg <- gg + facet_grid( . ~ factor(data_rate, levels=c('240 kbps','120 kbps','60 kbps','30 kbps','15 kbps')), scales = "free")
gg <- gg + facet_grid( type ~ ., scales = "free")
gg <- gg + coord_cartesian(xlim =c(0, 20), ylim = c(1, 100))
#gg <- gg + scale_x_continuous(breaks = seq(0, 200, len = 4))
#gg <- gg + scale_y_continuous(breaks = seq(0, 100, len = 10))

gg <- gg + ylab("Packet")
gg <- gg + xlab("Elapsed Time (sec)")
#gg <- gg + guides(shape = guide_legend(override.aes = list(size = 3)))
gg <- gg + theme(axis.text.x = element_text(size = 23, angle = 45, vjust = 0.5, hjust = 0.7),
                 axis.text.y = element_text(size = 24),
                 axis.title = element_text(size = 28),
                 axis.title.y = element_text(margin = margin(t = 0, r = 10, b = 0, l = 0)),
                 axis.title.x = element_text(margin = margin(t = 15, r = 0, b = 0, l = 0)),
                 strip.background = element_blank(),
                 strip.text = element_text(face = "bold", size = 19),
                 strip.placement = "outside",
                 legend.position = "bottom",
                 legend.background = element_rect(fill="transparent"),
                 legend.title = element_text(size = 23, face = "bold", colour = "black"),
                 legend.text=element_text(size=20, colour = "black"),
                 legend.title.align = 0.5)

theme_get()
theme_set(theme_bw())
print(gg)

ggsave(filename = "C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/plots/adaptive_comparison_uhf.png",plot=last_plot(), device="png", units = "mm", width = 400, height = 200, dpi = 600)
ggsave(filename = "C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/thesis_plots/adaptive_comparison_uhf.eps",plot=last_plot(), device="eps", units = "mm", width = 400, height = 200, dpi = 600)


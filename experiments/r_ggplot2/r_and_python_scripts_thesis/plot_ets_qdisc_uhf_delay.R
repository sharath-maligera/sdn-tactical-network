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


data_df_1 <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/with_shaping_and_ets_scheduling_no_timeout/plot_ets_qdisc_15_kbps.csv')
data_df_1$data_rate <- "15 kbps"
data_df_2 <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/with_shaping_and_ets_scheduling_no_timeout/plot_ets_qdisc_30_kbps.csv')
data_df_2$data_rate <- "30 kbps"
data_df_3 <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/with_shaping_and_ets_scheduling_no_timeout/plot_ets_qdisc_60_kbps.csv')
data_df_3$data_rate <- "60 kbps"
data_df_4 <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/with_shaping_and_ets_scheduling_no_timeout/plot_ets_qdisc_120_kbps.csv')
data_df_4$data_rate <- "120 kbps"
data_df_5 <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/with_shaping_and_ets_scheduling_no_timeout/plot_ets_qdisc_240_kbps.csv')
data_df_5$data_rate <- "240 kbps"

data_df <- rbind(data_df_1,data_df_2,data_df_3,data_df_4,data_df_5)

data_df$data_rate_f = factor(data_df$data_rate, levels=c('15 kbps','30 kbps','60 kbps','120 kbps','240 kbps'))

data_df$flow_id <- factor(data_df$flow_id, levels = c("6", "7", "8", "9", "1"), 
                          labels = c("Medical Evacuation", "Obstacle Alert", "Picture", "Chat", "FFT"))
colnames(data_df)[which(names(data_df) == "flow_id")] <- "Messages"


gg <- ggplot()
gg <- gg + geom_line(data = data_df, mapping = aes(x = packet_seq_no, y = packet_delay_in_secs, color=Messages, linetype=Messages))
gg <- gg + geom_point(data = data_df, mapping = aes(x = packet_seq_no, y = packet_delay_in_secs, color=Messages, shape=Messages), size = 3, stroke=1.3, alpha = 1)
gg <- gg + scale_linetype_manual(values=c("longdash", "twodash", "dashed","dotdash","dotted"))
gg <- gg + scale_shape_manual(values=c(1, 2, 3, 4, 5))
gg <- gg + scale_color_manual(values=c('grey25','tomato4', 'tomato', 'goldenrod', 'khaki4'))
gg <- gg + facet_grid( ~ data_rate_f)
gg <- gg + coord_cartesian()
gg <- gg + xlab("Packet")
gg <- gg + ylab("End-to-End Delay (sec)")
gg <- gg + theme(axis.text.x = element_text(size = 23, angle = 45, vjust = 0.5, hjust = 0.7),
                 axis.text.y = element_text(size = 24),
                 axis.title = element_text(size = 28),
                 axis.title.y = element_text(margin = margin(t = 0, r = 10, b = 0, l = 0)),
                 axis.title.x = element_text(margin = margin(t = 10, r = 0, b = 0, l = 0)),
                 strip.text = element_text(face = "bold", size = 23),
                 legend.position =  c(0.905, 0.8),
                 legend.background = element_rect(fill="transparent"),
                 legend.title = element_text(size = 22, face = "bold", colour = "black"),
                 legend.text=element_text(size=20, colour = "black"),
                 legend.title.align = 0.5)

theme_get()
theme_set(theme_bw())
print(gg)

ggsave(filename = "C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/plots/with_ets_qdisc_delay_uhf.png",plot=last_plot(), device="png", units = "mm", width = 400, height = 200, dpi = 600)
ggsave(filename = "C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/plots/with_ets_qdisc_delay_uhf.eps",plot=last_plot(), device="eps", units = "mm", width = 400, height = 200, dpi = 600)

rm(list = ls())
graphics.off()

library(ggplot2)
library(dplyr)
library(RColorBrewer)
library(wesanderson)
library(cowplot)
library(scales)
library(grid)

#brewer.pal.info
#display.brewer.all()
#display.brewer.all(type="seq")
#display.brewer.all(type="div")


data_df_0_6_wo_timeout <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data_icmcis/with_shaping_and_ets_scheduling_no_timeout/plot_ets_qdisc_0_6_kbps.csv')
data_df_0_6_wo_timeout$timeout <- "Without timeout"
data_df_1_2_wo_timeout <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data_icmcis/with_shaping_and_ets_scheduling_no_timeout/plot_ets_qdisc_1_2_kbps.csv')
data_df_1_2_wo_timeout$timeout <- "Without timeout"
data_df_2_4_wo_timeout <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data_icmcis/with_shaping_and_ets_scheduling_no_timeout/plot_ets_qdisc_2_4_kbps.csv')
data_df_2_4_wo_timeout$timeout <- "Without timeout"
data_df_4_8_wo_timeout <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data_icmcis/with_shaping_and_ets_scheduling_no_timeout/plot_ets_qdisc_4_8_kbps.csv')
data_df_4_8_wo_timeout$timeout <- "Without timeout"
data_df_9_6_wo_timeout <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data_icmcis/with_shaping_and_ets_scheduling_no_timeout/plot_ets_qdisc_9_6_kbps.csv')
data_df_9_6_wo_timeout$timeout <- "Without timeout"


data_df_0_6_with_timeout <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data_icmcis/with_shaping_and_ets_scheduling_with_timeout/plot_ets_qdisc_0_6_kbps.csv')
data_df_0_6_with_timeout$timeout <- "With timeout"
data_df_1_2_with_timeout <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data_icmcis/with_shaping_and_ets_scheduling_with_timeout/plot_ets_qdisc_1_2_kbps.csv')
data_df_1_2_with_timeout$timeout <- "With timeout"
data_df_2_4_with_timeout <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data_icmcis/with_shaping_and_ets_scheduling_with_timeout/plot_ets_qdisc_2_4_kbps.csv')
data_df_2_4_with_timeout$timeout <- "With timeout"
data_df_4_8_with_timeout <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data_icmcis/with_shaping_and_ets_scheduling_with_timeout/plot_ets_qdisc_4_8_kbps.csv')
data_df_4_8_with_timeout$timeout <- "With timeout"
data_df_9_6_with_timeout <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data_icmcis/with_shaping_and_ets_scheduling_with_timeout/plot_ets_qdisc_9_6_kbps.csv')
data_df_9_6_with_timeout$timeout <- "With timeout"


data_df_0_6_wo_timeout$datarate <- "0.6 kbps"
data_df_1_2_wo_timeout$datarate <- "1.2 kbps"
data_df_2_4_wo_timeout$datarate <- "2.4 kbps"
data_df_4_8_wo_timeout$datarate <- "4.8 kbps"
data_df_9_6_wo_timeout$datarate <- "9.6 kbps"
data_df_0_6_with_timeout$datarate <- "0.6 kbps"
data_df_1_2_with_timeout$datarate <- "1.2 kbps"
data_df_2_4_with_timeout$datarate <- "2.4 kbps"
data_df_4_8_with_timeout$datarate <- "4.8 kbps"
data_df_9_6_with_timeout$datarate <- "9.6 kbps"


data_df_0_6 <- rbind(data_df_0_6_wo_timeout,data_df_0_6_with_timeout)
data_df_0_6$timeout_f = factor(data_df_0_6$timeout, levels=c('Without timeout','With timeout'))

data_df_1_2 <- rbind(data_df_1_2_wo_timeout,data_df_1_2_with_timeout)
data_df_1_2$timeout_f = factor(data_df_1_2$timeout, levels=c('Without timeout','With timeout'))

data_df_2_4 <- rbind(data_df_2_4_wo_timeout,data_df_2_4_with_timeout)
data_df_2_4$timeout_f = factor(data_df_2_4$timeout, levels=c('Without timeout','With timeout'))

data_df_4_8 <- rbind(data_df_4_8_wo_timeout,data_df_4_8_with_timeout)
data_df_4_8$timeout_f = factor(data_df_4_8$timeout, levels=c('Without timeout','With timeout'))

data_df_9_6 <- rbind(data_df_9_6_wo_timeout,data_df_9_6_with_timeout)
data_df_9_6$timeout_f = factor(data_df_9_6$timeout, levels=c('Without timeout','With timeout'))


data_df_0_6$flow_id <- factor(data_df_0_6$flow_id, levels = c("1", "2", "3", "4", "5"), labels = c("Medical Evacuation", "Obstacle Alert", "Picture", "Chat", "FFT"))
colnames(data_df_0_6)[which(names(data_df_0_6) == "flow_id")] <- "Messages"

data_df_1_2$flow_id <- factor(data_df_1_2$flow_id, levels = c("1", "2", "3", "4", "5"), labels = c("Medical Evacuation", "Obstacle Alert", "Picture", "Chat", "FFT"))
colnames(data_df_1_2)[which(names(data_df_1_2) == "flow_id")] <- "Messages"

data_df_2_4$flow_id <- factor(data_df_2_4$flow_id, levels = c("1", "2", "3", "4", "5"), labels = c("Medical Evacuation", "Obstacle Alert", "Picture", "Chat", "FFT"))
colnames(data_df_2_4)[which(names(data_df_2_4) == "flow_id")] <- "Messages"

data_df_4_8$flow_id <- factor(data_df_4_8$flow_id, levels = c("1", "2", "3", "4", "5"), labels = c("Medical Evacuation", "Obstacle Alert", "Picture", "Chat", "FFT"))
colnames(data_df_4_8)[which(names(data_df_4_8) == "flow_id")] <- "Messages"

data_df_9_6$flow_id <- factor(data_df_9_6$flow_id, levels = c("1", "2", "3", "4", "5"), labels = c("Medical Evacuation", "Obstacle Alert", "Picture", "Chat", "FFT"))
colnames(data_df_9_6)[which(names(data_df_9_6) == "flow_id")] <- "Messages"


gg1 <- ggplot()
gg1 <- gg1 + geom_line(data = data_df_0_6, mapping = aes(x = packet_delay_in_secs, y = packet_seq_no, color=Messages, linetype=Messages))
gg1 <- gg1 + geom_point(data = data_df_0_6, mapping = aes(x = packet_delay_in_secs, y = packet_seq_no, color=Messages, shape=Messages), size = 3, stroke=1.3, alpha = 1)
gg1 <- gg1 + scale_x_continuous(n.breaks = 20)
gg1 <- gg1 + scale_y_continuous(n.breaks = 7)
gg1 <- gg1 + scale_linetype_manual(values=c("longdash", "twodash", "dashed","dotdash","dotted"))
gg1 <- gg1 + scale_shape_manual(values=c(1, 2, 3, 4, 5))
gg1 <- gg1 + scale_color_manual(values=c('grey40', 'tomato4','tomato', 'goldenrod', '#2C5F2DFF'))
gg1 <- gg1 + coord_cartesian()
gg1 <- gg1 + facet_grid( timeout_f ~ datarate)
gg1 <- gg1 + xlab("Elapsed Time (sec)")
gg1 <- gg1 + ylab("Packet")
gg1 <- gg1 + theme(axis.text.x = element_text(size = 23, angle = 45, vjust = 0.5, hjust = 0.7),
                 axis.text.y = element_text(size = 24),
                 axis.title = element_text(size = 28),
                 axis.title.y = element_text(margin = margin(t = 0, r = 10, b = 0, l = 0)),
                 axis.title.x = element_blank(),
                 strip.background = element_rect(colour = "white", fill = "#f0f0f0"),
                 strip.text = element_text(face = "bold", size = 20),
                 legend.position =  "none")

print(gg1)

gg2 <- ggplot()
gg2 <- gg2 + geom_line(data = data_df_1_2, mapping = aes(x = packet_delay_in_secs, y = packet_seq_no, color=Messages, linetype=Messages))
gg2 <- gg2 + geom_point(data = data_df_1_2, mapping = aes(x = packet_delay_in_secs, y = packet_seq_no, color=Messages, shape=Messages), size = 3, stroke=1.3, alpha = 1)
gg2 <- gg2 + scale_x_continuous(n.breaks = 20)
gg2 <- gg2 + scale_y_continuous(n.breaks = 7)
gg2 <- gg2 + scale_linetype_manual(values=c("longdash", "twodash", "dashed","dotdash","dotted"))
gg2 <- gg2 + scale_shape_manual(values=c(1, 2, 3, 4, 5))
gg2 <- gg2 + scale_color_manual(values=c('grey40', 'tomato4','tomato', 'goldenrod', '#2C5F2DFF'))
gg2 <- gg2 + coord_cartesian()
gg2 <- gg2 + facet_grid( timeout_f ~ datarate)
gg2 <- gg2 + xlab("Elapsed Time (sec)")
gg2 <- gg2 + ylab("Packet")
gg2 <- gg2 + theme(axis.text.x = element_text(size = 23, angle = 45, vjust = 0.5, hjust = 0.7),
                   axis.text.y = element_text(size = 24),
                   axis.title = element_text(size = 28),
                   axis.title.y = element_text(margin = margin(t = 0, r = 10, b = 0, l = 0)),
                   axis.title.x = element_blank(),
                   strip.background = element_rect(colour = "white", fill = "#f0f0f0"),
                   strip.text = element_text(face = "bold", size = 20),
                   legend.position =  "none")

gg3 <- ggplot()
gg3 <- gg3 + geom_line(data = data_df_2_4, mapping = aes(x = packet_delay_in_secs, y = packet_seq_no, color=Messages, linetype=Messages))
gg3 <- gg3 + geom_point(data = data_df_2_4, mapping = aes(x = packet_delay_in_secs, y = packet_seq_no, color=Messages, shape=Messages), size = 3, stroke=1.3, alpha = 1)
gg3 <- gg3 + scale_x_continuous(n.breaks = 20)
gg3 <- gg3 + scale_y_continuous(n.breaks = 7)
gg3 <- gg3 + scale_linetype_manual(values=c("longdash", "twodash", "dashed","dotdash","dotted"))
gg3 <- gg3 + scale_shape_manual(values=c(1, 2, 3, 4, 5))
gg3 <- gg3 + scale_color_manual(values=c('grey40', 'tomato4','tomato', 'goldenrod', '#2C5F2DFF'))
gg3 <- gg3 + coord_cartesian()
gg3 <- gg3 + facet_grid( timeout_f ~ datarate)
gg3 <- gg3 + xlab("Elapsed Time (sec)")
gg3 <- gg3 + ylab("Packet")
gg3 <- gg3 + theme(axis.text.x = element_text(size = 23, angle = 45, vjust = 0.5, hjust = 0.7),
                   axis.text.y = element_text(size = 24),
                   axis.title = element_text(size = 28),
                   axis.title.y = element_text(margin = margin(t = 0, r = 10, b = 0, l = 0)),
                   axis.title.x = element_blank(),
                   strip.background = element_rect(colour = "white", fill = "#f0f0f0"),
                   strip.text = element_text(face = "bold", size = 20),
                   legend.position =  "none")

gg4 <- ggplot()
gg4 <- gg4 + geom_line(data = data_df_4_8, mapping = aes(x = packet_delay_in_secs, y = packet_seq_no, color=Messages, linetype=Messages))
gg4 <- gg4 + geom_point(data = data_df_4_8, mapping = aes(x = packet_delay_in_secs, y = packet_seq_no, color=Messages, shape=Messages), size = 3, stroke=1.3, alpha = 1)
gg4 <- gg4 + scale_x_continuous(n.breaks = 20)
gg4 <- gg4 + scale_y_continuous(n.breaks = 7)
gg4 <- gg4 + scale_linetype_manual(values=c("longdash", "twodash", "dashed","dotdash","dotted"))
gg4 <- gg4 + scale_shape_manual(values=c(1, 2, 3, 4, 5))
gg4 <- gg4 + scale_color_manual(values=c('grey40', 'tomato4','tomato', 'goldenrod', '#2C5F2DFF'))
gg4 <- gg4 + coord_cartesian()
gg4 <- gg4 + facet_grid( timeout_f ~ datarate)
gg4 <- gg4 + xlab("Elapsed Time (sec)")
gg4 <- gg4 + ylab("Packet")
gg4 <- gg4 + theme(axis.text.x = element_text(size = 23, angle = 45, vjust = 0.5, hjust = 0.7),
                   axis.text.y = element_text(size = 24),
                   axis.title = element_text(size = 28),
                   axis.title.y = element_text(margin = margin(t = 0, r = 10, b = 0, l = 0)),
                   axis.title.x = element_blank(),
                   strip.background = element_rect(colour = "white", fill = "#f0f0f0"),
                   strip.text = element_text(face = "bold", size = 20),
                   legend.position =  "none")

gg5 <- ggplot()
gg5 <- gg5 + geom_line(data = data_df_9_6, mapping = aes(x = packet_delay_in_secs, y = packet_seq_no, color=Messages, linetype=Messages))
gg5 <- gg5 + geom_point(data = data_df_9_6, mapping = aes(x = packet_delay_in_secs, y = packet_seq_no, color=Messages, shape=Messages), size = 3, stroke=1.3, alpha = 1)
gg5 <- gg5 + scale_x_continuous(n.breaks = 20)
gg5 <- gg5 + scale_y_continuous(n.breaks = 7)
gg5 <- gg5 + scale_linetype_manual(values=c("longdash", "twodash", "dashed","dotdash","dotted"))
gg5 <- gg5 + scale_shape_manual(values=c(1, 2, 3, 4, 5))
gg5 <- gg5 + scale_color_manual(values=c('grey40', 'tomato4','tomato', 'goldenrod', '#2C5F2DFF'))
gg5 <- gg5 + coord_cartesian()
gg5 <- gg5 + facet_grid( timeout_f ~ datarate)
gg5 <- gg5 + xlab("Elapsed Time (sec)")
gg5 <- gg5 + ylab("Packet")
gg5 <- gg5 + theme(axis.text.x = element_text(size = 23, angle = 45, vjust = 0.5, hjust = 0.7),
                   axis.text.y = element_text(size = 24),
                   axis.title = element_text(size = 28),
                   axis.title.y = element_text(margin = margin(t = 0, r = 10, b = 0, l = 0)),
                   axis.title.x = element_text(margin = margin(t = 15, r = 0, b = 0, l = 0)),
                   strip.background = element_rect(colour = "white", fill = "#f0f0f0"),
                   strip.text = element_text(face = "bold", size = 20),
                   legend.position =  "bottom",
                   legend.background = element_rect(fill="transparent"),
                   legend.title = element_text(size = 28, face = "bold", colour = "black"),
                   legend.text=element_text(size=28, colour = "black"),
                   legend.title.align = 0.5)

plot_grid(gg1, gg2, gg3, gg4, gg5, align = "v", ncol = 1, nrow = 5, rel_heights = c(0.77,0.77,0.77,0.77,1))

theme_get()
theme_set(theme_bw())

ggsave(filename = "C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/plots/with_ets_with_vs_wo_timeout_all_vhf.png",plot=last_plot(), device="png", units = "mm", width = 400, height = 400, dpi = 600)
#ggsave(filename = "C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/plots/with_ets_with_vs_wo_timeout_all_vhf.eps",plot=last_plot(), device="eps", units = "mm", width = 400, height = 400)


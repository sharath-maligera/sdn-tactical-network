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


data_df_0_6_wo_timeout <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/with_shaping_and_ets_scheduling_no_timeout/plot_ets_qdisc_0_6_kbps.csv')
data_df_0_6_wo_timeout$timeout <- "Without ToE QoS"
data_df_1_2_wo_timeout <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/with_shaping_and_ets_scheduling_no_timeout/plot_ets_qdisc_1_2_kbps.csv')
data_df_1_2_wo_timeout$timeout <- "Without ToE QoS"
data_df_2_4_wo_timeout <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/with_shaping_and_ets_scheduling_no_timeout/plot_ets_qdisc_2_4_kbps.csv')
data_df_2_4_wo_timeout$timeout <- "Without ToE QoS"
data_df_4_8_wo_timeout <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/with_shaping_and_ets_scheduling_no_timeout/plot_ets_qdisc_4_8_kbps.csv')
data_df_4_8_wo_timeout$timeout <- "Without ToE QoS"
data_df_9_6_wo_timeout <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/with_shaping_and_ets_scheduling_no_timeout/plot_ets_qdisc_9_6_kbps.csv')
data_df_9_6_wo_timeout$timeout <- "Without ToE QoS"


data_df_0_6_with_timeout <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/with_shaping_and_ets_scheduling_with_timeout/plot_ets_qdisc_0_6_kbps.csv')
data_df_0_6_with_timeout$timeout <- "With ToE QoS"
data_df_1_2_with_timeout <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/with_shaping_and_ets_scheduling_with_timeout/plot_ets_qdisc_1_2_kbps.csv')
data_df_1_2_with_timeout$timeout <- "With ToE QoS"
data_df_2_4_with_timeout <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/with_shaping_and_ets_scheduling_with_timeout/plot_ets_qdisc_2_4_kbps.csv')
data_df_2_4_with_timeout$timeout <- "With ToE QoS"
data_df_4_8_with_timeout <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/with_shaping_and_ets_scheduling_with_timeout/plot_ets_qdisc_4_8_kbps.csv')
data_df_4_8_with_timeout$timeout <- "With ToE QoS"
data_df_9_6_with_timeout <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/with_shaping_and_ets_scheduling_with_timeout/plot_ets_qdisc_9_6_kbps.csv')
data_df_9_6_with_timeout$timeout <- "With ToE QoS"


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
data_df_0_6$timeout_f = factor(data_df_0_6$timeout, levels=c('Without ToE QoS','With ToE QoS'))

data_df_1_2 <- rbind(data_df_1_2_wo_timeout,data_df_1_2_with_timeout)
data_df_1_2$timeout_f = factor(data_df_1_2$timeout, levels=c('Without ToE QoS','With ToE QoS'))

data_df_2_4 <- rbind(data_df_2_4_wo_timeout,data_df_2_4_with_timeout)
data_df_2_4$timeout_f = factor(data_df_2_4$timeout, levels=c('Without ToE QoS','With ToE QoS'))

data_df_4_8 <- rbind(data_df_4_8_wo_timeout,data_df_4_8_with_timeout)
data_df_4_8$timeout_f = factor(data_df_4_8$timeout, levels=c('Without ToE QoS','With ToE QoS'))

data_df_9_6 <- rbind(data_df_9_6_wo_timeout,data_df_9_6_with_timeout)
data_df_9_6$timeout_f = factor(data_df_9_6$timeout, levels=c('Without ToE QoS','With ToE QoS'))


data_df_0_6$flow_id <- factor(data_df_0_6$flow_id, levels = c("1", "2", "3", "4", "5"), labels = c("Medical Evac.", "Obstacle Alert", "Picture", "Chat", "FFT"))
colnames(data_df_0_6)[which(names(data_df_0_6) == "flow_id")] <- "Messages"

data_df_1_2$flow_id <- factor(data_df_1_2$flow_id, levels = c("1", "2", "3", "4", "5"), labels = c("Medical Evac.", "Obstacle Alert", "Picture", "Chat", "FFT"))
colnames(data_df_1_2)[which(names(data_df_1_2) == "flow_id")] <- "Messages"

data_df_2_4$flow_id <- factor(data_df_2_4$flow_id, levels = c("1", "2", "3", "4", "5"), labels = c("Medical Evac.", "Obstacle Alert", "Picture", "Chat", "FFT"))
colnames(data_df_2_4)[which(names(data_df_2_4) == "flow_id")] <- "Messages"

data_df_4_8$flow_id <- factor(data_df_4_8$flow_id, levels = c("1", "2", "3", "4", "5"), labels = c("Medical Evac.", "Obstacle Alert", "Picture", "Chat", "FFT"))
colnames(data_df_4_8)[which(names(data_df_4_8) == "flow_id")] <- "Messages"

data_df_9_6$flow_id <- factor(data_df_9_6$flow_id, levels = c("1", "2", "3", "4", "5"), labels = c("Medical Evac.", "Obstacle Alert", "Picture", "Chat", "FFT"))
colnames(data_df_9_6)[which(names(data_df_9_6) == "flow_id")] <- "Messages"





data_df <- rbind(data_df_0_6,data_df_1_2,data_df_2_4,data_df_4_8,data_df_9_6)

gg1 <- ggplot()
#gg1 <- gg1 + geom_line(data = data_df, mapping = aes(x = packet_delay_in_secs, y = packet_seq_no, color=Messages, linetype=Messages))
gg1 <- gg1 + geom_point(data = data_df, mapping = aes(x = packet_delay_in_secs, y = packet_seq_no, color=Messages, shape=Messages), size = 0.8, stroke=1, alpha = .8)
gg1 <- gg1 + scale_x_continuous(n.breaks = 5)
gg1 <- gg1 + scale_y_continuous(n.breaks = 7)
gg1 <- gg1 + scale_linetype_manual(values=c("longdash", "twodash", "dashed","dotdash","dotted"))
gg1 <- gg1 + scale_shape_manual(values=c(16, 17, 18,4,5))
gg1 <- gg1 + scale_color_manual(values=c('#1e2240', '#607dab','#b5c9d5', '#FFE77AFF', '#2C5F2DFF'))
#gg1 <- gg1 + scale_color_grey(start = 0.8, end = .2)
gg1 <- gg1 + coord_cartesian()
gg1 <- gg1 + facet_grid( timeout_f ~ datarate, scales="free")#, ncol = 2)
gg1 <- gg1 + xlab("Time (sec)")
gg1 <- gg1 + ylab("Packet")
#gg1 <- gg1 + theme(axis.text.x = element_text(size = 23, angle = 45, vjust = 0.5, hjust = 0.7),
#                 axis.text.y = element_text(size = 24),
#                 axis.title = element_text(size = 28),
#                 axis.title.y = element_text(margin = margin(t = 0, r = 10, b = 0, l = 0)),
#                 axis.title.x = element_blank(),
#                 strip.background = element_rect(colour = "white", fill = "#f0f0f0"),
#                 strip.text = element_text(face = "bold", size = 20),
#                 legend.position =  "none")
gg1 <- gg1 + guides(shape = guide_legend(override.aes = list(size = 3)))
gg1 <- gg1 + theme(legend.position =  "bottom",axis.text.x = element_text(angle = 30),
                   axis.text=element_text(size=12),
                   axis.title=element_text(size=12),legend.title=element_text(size=12), 
                   legend.text=element_text(size=12),strip.text.x = element_text(size = 10),strip.text.y = element_text(size = 12),
                   strip.background = element_blank(), strip.placement = "outside")

theme_get()
theme_set(theme_bw())
print(gg1)

#7x4

ggsave(filename = "C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/plots/with_ets_with_vs_wo_timeout_all_vhf.png",plot=gg1, device="png", units = "mm", width = 400, height = 300, dpi = 600)
ggsave(filename = "C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/plots/with_ets_with_vs_wo_timeout_all_vhf.eps",plot=gg1, device="eps", units = "mm", width = 400, height = 300)


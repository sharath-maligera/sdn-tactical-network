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


data_df_0_6_wo_timeout <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/with_shaping_and_ets_scheduling_no_timeout/plot_ets_qdisc_0_6_kbps.csv')
data_df_0_6_wo_timeout$timeout <- "Without timeout"
data_df_1_2_wo_timeout <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/with_shaping_and_ets_scheduling_no_timeout/plot_ets_qdisc_1_2_kbps.csv')
data_df_1_2_wo_timeout$timeout <- "Without timeout"
data_df_2_4_wo_timeout <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/with_shaping_and_ets_scheduling_no_timeout/plot_ets_qdisc_2_4_kbps.csv')
data_df_2_4_wo_timeout$timeout <- "Without timeout"
data_df_4_8_wo_timeout <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/with_shaping_and_ets_scheduling_no_timeout/plot_ets_qdisc_4_8_kbps.csv')
data_df_4_8_wo_timeout$timeout <- "Without timeout"
data_df_9_6_wo_timeout <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/with_shaping_and_ets_scheduling_no_timeout/plot_ets_qdisc_9_6_kbps.csv')
data_df_9_6_wo_timeout$timeout <- "Without timeout"

data_df_0_6_with_timeout <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/with_shaping_and_ets_scheduling_with_timeout/plot_ets_qdisc_0_6_kbps.csv')
data_df_0_6_with_timeout$timeout <- "With timeout"
data_df_1_2_with_timeout <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/with_shaping_and_ets_scheduling_with_timeout/plot_ets_qdisc_1_2_kbps.csv')
data_df_1_2_with_timeout$timeout <- "With timeout"
data_df_2_4_with_timeout <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/with_shaping_and_ets_scheduling_with_timeout/plot_ets_qdisc_2_4_kbps.csv')
data_df_2_4_with_timeout$timeout <- "With timeout"
data_df_4_8_with_timeout <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/with_shaping_and_ets_scheduling_with_timeout/plot_ets_qdisc_4_8_kbps.csv')
data_df_4_8_with_timeout$timeout <- "With timeout"
data_df_9_6_with_timeout <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/with_shaping_and_ets_scheduling_with_timeout/plot_ets_qdisc_9_6_kbps.csv')
data_df_9_6_with_timeout$timeout <- "With timeout"


data_df_0_6 <- rbind(data_df_0_6_wo_timeout,data_df_0_6_with_timeout)
data_df_0_6$timeout_f = factor(data_df_0_6$timeout, levels=c('Without timeout','With timeout'))


data_df_0_6$flow_id <- factor(data_df_0_6$flow_id, levels = c("1", "2", "3", "4", "5"), labels = c("Medical Evacuation", "Obstacle Alert", "Picture", "Chat", "FFT"))
colnames(data_df_0_6)[which(names(data_df_0_6) == "flow_id")] <- "Messages"

gg1 <- ggplot()
gg1 <- gg1 + geom_line(data = data_df_0_6, mapping = aes(x = packet_delay_in_secs, y = packet_seq_no, color=Messages, linetype=Messages))
gg1 <- gg1 + geom_point(data = data_df_0_6, mapping = aes(x = packet_delay_in_secs, y = packet_seq_no, color=Messages, shape=Messages), size = 3, stroke=1.3, alpha = 1)
gg1 <- gg1 + scale_x_continuous(n.breaks = 20)
gg1 <- gg1 + scale_y_continuous(n.breaks = 7)
gg1 <- gg1 + scale_linetype_manual(values=c("longdash", "twodash", "dashed","dotdash","dotted"))
gg1 <- gg1 + scale_shape_manual(values=c(1, 2, 3, 4, 5))
gg1 <- gg1 + scale_color_manual(values=c('grey25','tomato4', 'tomato', 'goldenrod', 'khaki4'))
gg1 <- gg1 + coord_cartesian()
gg1 <- gg1 + facet_grid( timeout_f ~ .)
gg1 <- gg1 + xlab("Elapsed Time (sec)")
gg1 <- gg1 + ylab("Packet")
gg1 <- gg1 + theme(axis.text.x = element_text(size = 23, angle = 45, vjust = 0.5, hjust = 0.7),
                 axis.text.y = element_text(size = 24),
                 axis.title = element_text(size = 28),
                 axis.title.y = element_text(margin = margin(t = 0, r = 10, b = 0, l = 0)),
                 axis.title.x = element_text(margin = margin(t = 15, r = 0, b = 0, l = 0)),
                 strip.text = element_text(face = "bold", size = 23),
                 legend.position =  c(0.85, 0.3),
                 legend.background = element_rect(fill="transparent"),
                 legend.title = element_text(size = 22, face = "bold", colour = "black"),
                 legend.text=element_text(size=20, colour = "black"),
                 legend.title.align = 0.5)



theme_get()
theme_set(theme_bw())
print(gg1)

ggsave(filename = "C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/plots/with_ets_with_vs_wo_timeout.png",plot=last_plot(), device="png", units = "mm", width = 400, height = 200, dpi = 600)
ggsave(filename = "C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/plots/with_ets_with_vs_wo_timeout.eps",plot=last_plot(), device="eps", units = "mm", width = 400, height = 200, dpi = 600)

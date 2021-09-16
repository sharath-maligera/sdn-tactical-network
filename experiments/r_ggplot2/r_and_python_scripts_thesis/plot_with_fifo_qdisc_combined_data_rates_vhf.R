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


#data_df_1 <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/no_adaptive_no_changing_/h2_data_9_6_kbps.csv')
#data_df_1$data_rate <- "9.6 kbps"
#data_df_1$shaping <- "Without Shaping"
#data_df_1_1 <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/no_adaptive_no_changing_ETS_both_end/h2_data_9_6_kbps.csv')
#data_df_1_1$data_rate <- "9.6 kbps"
#data_df_1_1$shaping <- "With Shaping"
#data_df_2 <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/no_adaptive_no_changing_ETS/h2_data_4_8_kbps.csv')
#data_df_2$data_rate <- "4.8 kbps"
#data_df_2$shaping <- "Without Shaping"
#data_df_2_1 <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/no_adaptive_no_changing_ETS_both_end/h2_data_4_8_kbps.csv')
#data_df_2_1$data_rate <- "4.8 kbps"
#data_df_2_1$shaping <- "With Shaping"
#data_df_3 <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/no_adaptive_no_changing_ETS/h2_data_2_4_kbps.csv')
#data_df_3$data_rate <- "2.4 kbps"
#data_df_3$shaping <- "Without Shaping"
#data_df_3_1 <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/no_adaptive_no_changing_ETS_both_end/h2_data_2_4_kbps.csv')
#data_df_3_1$data_rate <- "2.4 kbps"
#data_df_3_1$shaping <- "With Shaping"
#data_df_4 <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/no_adaptive_no_changing_ETS/h2_data_1_2_kbps.csv')
#data_df_4$data_rate <- "1.2 kbps"
#data_df_4$shaping <- "Without Shaping"
#data_df_4_1 <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/no_adaptive_no_changing_ETS_both_end/h2_data_1_2_kbps.csv')
#data_df_4_1$data_rate <- "1.2 kbps"
#data_df_4_1$shaping <- "With Shaping"
#data_df_5 <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/no_adaptive_no_changing_ETS/h2_data_0_6_kbps.csv')
#data_df_5$data_rate <- "0.6 kbps"
#data_df_5$shaping <- "Without Shaping"
#data_df_5_1 <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/no_adaptive_no_changing_ETS_both_end/h2_data_0_6_kbps.csv')
#data_df_5_1$data_rate <- "0.6 kbps"
#data_df_5_1$shaping <- "With Shaping"
#
#data_df <- rbind(data_df_1,data_df_1_1,data_df_2,data_df_2_1,data_df_3,data_df_3_1,data_df_4,data_df_4_1,data_df_5,data_df_5_1)


data_df_1 <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/no_adaptive_no_changing_ETS_both_end/h2_data_9_6_kbps.csv')
data_df_1$data_rate <- "9.6 kbps"

data_df_2 <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/no_adaptive_no_changing_ETS_both_end/h2_data_4_8_kbps.csv')
data_df_2$data_rate <- "4.8 kbps"

data_df_3 <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/no_adaptive_no_changing_ETS_both_end/h2_data_2_4_kbps.csv')
data_df_3$data_rate <- "2.4 kbps"


data_df_4 <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/no_adaptive_no_changing_ETS_both_end/h2_data_1_2_kbps.csv')
data_df_4$data_rate <- "1.2 kbps"

data_df_5 <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/no_adaptive_no_changing_ETS_both_end/h2_data_0_6_kbps.csv')
data_df_5$data_rate <- "0.6 kbps"


data_df <- rbind(data_df_1,data_df_2,data_df_3,data_df_4,data_df_5)


data_df$flow_id <- factor(data_df$flow_id, levels = c("1", "2", "3", "4", "5"),
                          labels = c("Medical Evacuation", "Obstacle Alert", "Picture", "Chat", "FFT"))
colnames(data_df)[which(names(data_df) == "flow_id")] <- "Messages"


gg <- ggplot()
gg <- gg + geom_line(data = data_df, mapping = aes(x = packet_seq_no, y = packet_delay_in_secs, color=Messages, linetype=Messages))
gg <- gg + geom_point(data = data_df, mapping = aes(x = packet_seq_no, y = packet_delay_in_secs, color=Messages, shape=Messages), size = 3, stroke=1.3, alpha = 1)
gg <- gg + scale_linetype_manual(values=c("longdash", "twodash", "dashed","dotdash","dotted"))
gg <- gg + scale_shape_manual(values=c(1, 2, 3, 4, 5))
#gg <- gg + scale_color_manual(values=c('#1e2240', '#607dab','#b5c9d5', '#FFE77AFF', '#2C5F2DFF'))
#gg <- gg + scale_color_manual(values=c('#1f1f1f','#660000', '#EA9999', '#E69138', '#B4A7D6'))
gg <- gg + scale_color_manual(values=c('grey40','tomato4', 'tomato', 'goldenrod', '#2C5F2DFF'))
gg <- gg + facet_grid( . ~ factor(data_rate, levels=c('0.6 kbps','1.2 kbps','2.4 kbps','4.8 kbps','9.6 kbps')), scales = "free")
gg <- gg + coord_cartesian()
gg <- gg + xlab("Packet")
gg <- gg + ylab("End-to-End Delay (sec)")
#gg <- gg + guides(shape = guide_legend(override.aes = list(size = 3)))
gg <- gg + theme(axis.text.x = element_text(size = 23, angle = 45, vjust = 0.5, hjust = 0.7),
                 axis.text.y = element_text(size = 24),
                 axis.title = element_text(size = 28),
                 axis.title.y = element_text(margin = margin(t = 0, r = 10, b = 0, l = 0)),
                 axis.title.x = element_text(margin = margin(t = 15, r = 0, b = 0, l = 0)),
                 strip.background = element_rect(colour = "black", fill = "#f0f0f0"),
                 strip.text = element_text(face = "bold", size = 22),
                 legend.position = "bottom",
                 legend.background = element_rect(fill="transparent"),
                 legend.title = element_text(size = 23, face = "bold", colour = "black"),
                 legend.text=element_text(size=20, colour = "black"),
                 legend.title.align = 0.5)

theme_get()
theme_set(theme_bw())
print(gg)

ggsave(filename = "C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/plots/with_ets_qdisc_no_timeout.png",plot=last_plot(), device="png", units = "mm", width = 400, height = 200, dpi = 600)
ggsave(filename = "C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/thesis_plots/with_ets_qdisc_no_timeout_vhf.eps",plot=last_plot(), device="eps", units = "mm", width = 400, height = 180, dpi = 600)

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


data_df_0_6 <- read.csv(file = '../data/with_shaping_and_fifo_scheduling_no_timeout/plot_fifo_qdisc_0_6_kbps.csv')
data_df_0_6$data_rate <- "0.6 kbps"
data_df_1_2 <- read.csv(file = '../data/with_shaping_and_fifo_scheduling_no_timeout/plot_fifo_qdisc_1_2_kbps.csv')
data_df_1_2$data_rate <- "1.2 kbps"
data_df_2_4 <- read.csv(file = '../data/with_shaping_and_fifo_scheduling_no_timeout/plot_fifo_qdisc_2_4_kbps.csv')
data_df_2_4$data_rate <- "2.4 kbps"
data_df_4_8 <- read.csv(file = '../data/with_shaping_and_fifo_scheduling_no_timeout/plot_fifo_qdisc_4_8_kbps.csv')
data_df_4_8$data_rate <- "4.8 kbps"
data_df_9_6 <- read.csv(file = '../data/with_shaping_and_fifo_scheduling_no_timeout/plot_fifo_qdisc_9_6_kbps.csv')
data_df_9_6$data_rate <- "9.6 kbps"

data_df <- rbind(data_df_0_6,data_df_1_2,data_df_2_4,data_df_4_8,data_df_9_6)

data_df$flow_id <- factor(data_df$flow_id, levels = c("1", "2", "3", "4", "5"), 
                          labels = c("Medical Evac.", "Obstacle Alert", "Picture", "Chat", "FFT"))
colnames(data_df)[which(names(data_df) == "flow_id")] <- "Messages"


gg <- ggplot()
#gg <- gg + geom_line(data = data_df, mapping = aes(x = packet_seq_no, y = packet_delay_in_secs, color=Messages, linetype=Messages))
gg <- gg + geom_point(data = data_df, mapping = aes(x = packet_seq_no, y = packet_delay_in_secs, color=Messages, shape=Messages), size = 0.8, stroke=1, alpha = .8)
gg <- gg + scale_linetype_manual(values=c("longdash", "twodash", "dashed","dotdash","dotted"))
gg <- gg + scale_shape_manual(values=c(16, 17, 18,4,5))
gg <- gg + scale_color_manual(values=c('#1e2240', '#607dab','#b5c9d5', '#FFE77AFF', '#2C5F2DFF'))
gg <- gg + facet_grid( ~ data_rate, scales = "free")
gg <- gg + coord_cartesian()
gg <- gg + xlab("Packet")
gg <- gg + ylab("End-to-End Delay (sec)")
# gg <- gg + theme(axis.text.x = element_text(size = 23, angle = 45, vjust = 0.5, hjust = 0.7),
#                  axis.text.y = element_text(size = 24),
#                  axis.title = element_text(size = 28),
#                  axis.title.y = element_text(margin = margin(t = 0, r = 10, b = 0, l = 0)),
#                  axis.title.x = element_text(margin = margin(t = 15, r = 0, b = 0, l = 0)),
#                  strip.background = element_rect(colour = "black", fill = "#f0f0f0"),
#                  strip.text = element_text(face = "bold", size = 23),
#                  legend.position =  c(0.905, 0.8),
#                  legend.background = element_rect(fill="transparent"),
#                  legend.title = element_text(size = 23, face = "bold", colour = "black"),
#                  legend.text=element_text(size=20, colour = "black"),
#                  legend.title.align = 0.5)
gg <- gg + guides(shape = guide_legend(override.aes = list(size = 3)))
gg <- gg + theme(legend.position = "bottom",axis.text.x = element_text(angle = 45, hjust=1),
                   axis.text=element_text(size=12),legend.background = element_rect(fill="transparent"),
                   axis.title=element_text(size=12),legend.title=element_text(size=12), 
                   legend.text=element_text(size=12),strip.text.x = element_text(size = 10),
                   strip.background = element_blank(), strip.placement = "outside")


theme_get()
theme_set(theme_bw())
print(gg)

#7x3.5

#ggsave(filename = "../plots/with_fifo_qdisc_no_timeout.png",plot=last_plot(), device="png", units = "mm", width = 400, height = 200, dpi = 600)
#ggsave(filename = "../plots/with_fifo_qdisc_no_timeout.eps",plot=last_plot(), device="eps", units = "mm", width = 400, height = 200, dpi = 600)

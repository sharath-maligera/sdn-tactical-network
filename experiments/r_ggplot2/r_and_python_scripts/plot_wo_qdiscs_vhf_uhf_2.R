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


data_df_vhf <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/without_qdiscs/plot_wo_qdisc_vhf_exp_1.csv')
data_df_vhf$data_rate <- "VHF"

data_df_uhf <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/without_qdiscs/plot_wo_qdisc_uhf_exp_1.csv')
data_df_uhf$data_rate <- "UHF"

data_df_vhf$flow_id <- factor(data_df_vhf$flow_id, levels = c("1", "2", "3", "4", "5"),
                          labels = c("Medical Evacuation", "Obstacle Alert", "Picture", "Chat", "FFT"))
colnames(data_df_vhf)[which(names(data_df_vhf) == "flow_id")] <- "Messages"

data_df_uhf$flow_id <- factor(data_df_uhf$flow_id, levels = c("6", "7", "8", "9", "1"),
                          labels = c("Medical Evacuation", "Obstacle Alert", "Picture", "Chat", "FFT"))
colnames(data_df_uhf)[which(names(data_df_uhf) == "flow_id")] <- "Messages"

data_df <- rbind(data_df_vhf,data_df_uhf)
data_df$data_rate_f = factor(data_df$data_rate, levels=c('VHF','UHF'))

gg <- ggplot()
#gg <- gg + geom_line(data = data_df, mapping = aes(x = packet_seq_no, y = packet_delay_in_secs, color=Messages, linetype=Messages))
gg <- gg + geom_point(data = data_df, mapping = aes(x = packet_seq_no, y = packet_delay_in_secs, color=Messages, shape=Messages), size = 0.8, stroke=1, alpha = .8)
gg <- gg + scale_linetype_manual(values=c("longdash", "twodash", "dashed","dotdash","dotted"))
gg <- gg + scale_shape_manual(values=c(1, 2, 3, 4, 5))
gg <- gg + scale_color_manual(values=c('#1e2240', '#607dab','#b5c9d5', '#FFE77AFF', '#2C5F2DFF'))
gg <- gg + facet_grid(  ~ data_rate_f, scales = "free")
gg <- gg + coord_cartesian()
gg <- gg + xlab("Packet")
gg <- gg + ylab("End-to-End Delay (sec)")
# gg <- gg + theme(axis.text.x = element_text(size = 24),
#                    axis.text.y = element_text(size = 24),
#                    axis.title = element_text(size = 28),
#                    axis.title.y = element_text(margin = margin(t = 0, r = 10, b = 0, l = 0)),
#                    axis.title.x = element_text(margin = margin(t = 15, r = 0, b = 0, l = 0)),
#                    strip.background = element_rect(colour = "black", fill = "#f0f0f0"),
#                    strip.text = element_text(face = "bold", size = 23),
#                    legend.position =  c(0.17,0.8),
#                    legend.background = element_rect(fill="transparent"),
#                    legend.title = element_text(size = 24, face = "bold", colour = "black"),
#                    legend.text=element_text(size=20, colour = "black"),
#                    legend.title.align = 0.5)
gg <- gg + guides(shape = guide_legend(override.aes = list(size = 3)))
gg <- gg + theme(legend.position = "bottom", axis.text.x = element_text(angle = 0),
                 axis.text=element_text(size=15),legend.background = element_rect(fill="transparent"),
                 axis.title=element_text(size=13),legend.title=element_text(size=14), 
                 legend.text=element_text(size=14),strip.text.x = element_text(size = 14),strip.text.y = element_text(size = 14),
                 strip.background = element_blank(), strip.placement = "outside")
gg <- gg + theme(legend.title=element_blank())

theme_get()
theme_set(theme_bw())
print(gg)

#3.0*7.9in

#ggsave(filename = "C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/plots/wo_qdisc_vhf_uhf.png",plot=last_plot(), device="png", units = "mm", width = 400, height = 160, dpi = 600)
#ggsave(filename = "C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/plots/wo_qdisc_vhf_uhf.eps",plot=last_plot(), device="eps", units = "mm", width = 400, height = 160, dpi = 600)


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


data_df<- read.csv(file = '../data/without_qdiscs/plot_wo_qdisc_no_delay_old.csv')

data_df$flow_id <- factor(data_df$flow_id, levels = c("1", "2", "3", "4", "5"),
                          labels = c("Medical Evacuation", "Obstacle Alert", "Picture", "Chat", "FFT"))
colnames(data_df)[which(names(data_df) == "flow_id")] <- "Messages"

gg <- ggplot()
gg <- gg + geom_line(data = data_df, mapping = aes(x = packet_seq_no, y = packet_delay_in_secs, color=Messages, linetype=Messages))
gg <- gg + geom_point(data = data_df, mapping = aes(x = packet_seq_no, y = packet_delay_in_secs, color=Messages, shape=Messages), size = 1, stroke=1, alpha = .8)
gg <- gg + scale_linetype_manual(values=c("longdash", "twodash", "dashed","dotdash","dotted"))
gg <- gg + scale_shape_manual(values=c(16, 17, 18,4,5))
gg <- gg + scale_color_manual(values=c('#1e2240', '#607dab','#b5c9d5', '#FFE77AFF', '#2C5F2DFF'))
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
#                    legend.position =  c(0.8,0.78),
#                    legend.background = element_rect(fill="transparent"),
#                    legend.title = element_text(size = 24, face = "bold", colour = "black"),
#                    legend.text=element_text(size=20, colour = "black"),
#                    legend.title.align = 0.5)
gg <- gg + guides(shape = guide_legend(override.aes = list(size = 1)))
gg <- gg + theme(legend.position = c(0.8,0.68),axis.text.x = element_text(angle = 0),
                 axis.text=element_text(size=12),legend.background = element_rect(fill="transparent"),
                 axis.title=element_text(size=12),legend.title=element_text(size=12), 
                 legend.text=element_text(size=12),
                 strip.background = element_blank(), strip.placement = "outside")
gg <- gg + theme(legend.title=element_blank())

theme_get()
theme_set(theme_bw())
print(gg)

#ggsave(filename = "../plots/wo_qdisc_no_delay.png",plot=last_plot(), device="png", units = "mm", width = 400, height = 150, dpi = 600)
#ggsave(filename = "../plots/wo_qdisc_no_delay.eps",plot=last_plot(), device="eps", units = "mm", width = 400, height = 150, dpi = 600)


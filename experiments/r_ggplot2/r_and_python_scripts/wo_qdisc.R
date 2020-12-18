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


data_df <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/without qdiscs/data_wo_qdisc.csv')

data_df$flow_id <- factor(data_df$flow_id, levels = c("1", "2", "3", "4", "5"), 
                          labels = c("Medical Evacuation", "Obstacle Alert", "Picture", "Chat", "FFT"))
colnames(data_df)[which(names(data_df) == "flow_id")] <- "Messages"


gg <- ggplot()
gg <- gg + geom_line(data = data_df, mapping = aes(x = packet_seq_no, y = packet_delay_in_secs, color=Messages, linetype=Messages))
gg <- gg + geom_point(data = data_df, mapping = aes(x = packet_seq_no, y = packet_delay_in_secs, color=Messages, shape=Messages), size = 3, stroke=1.3, alpha = 1)
gg <- gg + scale_linetype_manual(values=c("longdash", "twodash", "dashed","dotdash","dotted"))
gg <- gg + scale_shape_manual(values=c(1, 2, 3, 4, 5))
gg <- gg + scale_color_manual(values=c('grey40','tomato4', 'tomato', 'goldenrod', 'gainsboro'))
gg <- gg + coord_cartesian()
gg <- gg + xlab("Packet")
gg <- gg + ylab("End-to-End Delay (sec)")
gg <- gg + theme(axis.text = element_text(size = 12),
                 axis.title = element_text(size = 16),
                 axis.title.y = element_text(margin = margin(t = 0, r = 20, b = 0, l = 0)),
                 axis.title.x = element_text(margin = margin(t = 20, r = 0, b = 0, l = 0)),
                 strip.text = element_text(face = "bold", size = 9),
                 legend.position = c(0.9, 0.8),
                 legend.background = element_rect(fill="transparent"),
                 legend.title = element_text(size = 12, face = "bold", colour = "black"),
                 legend.title.align = 0.5)

theme_get()
theme_set(theme_bw())
print(gg)

ggsave(filename = "C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/plots/without_qdisc.png",plot=last_plot(), device="png", units = "mm", width = 300, height = 200, dpi = 600)
ggsave(filename = "C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/plots/without_qdisc.eps",plot=last_plot(), device="eps", units = "mm", width = 300, height = 200, dpi = 600)


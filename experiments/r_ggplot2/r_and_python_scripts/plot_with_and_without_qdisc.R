# Data visualization with ggplot2 & grammar of graphics


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


data_df <- read.csv(file = 'data_with_and_without_qdisc.csv')

data_df$flow_id <- factor(data_df$flow_id, levels = c("1", "2", "3", "4", "5"), 
                  labels = c("Medical Evacuation", "Obstacle Alert", "Video", "Picture", "FFT"))
data_df$label <- factor(data_df$label, levels = c("with_out_qdisc", "with_qdisc"),
                  labels = c("Without Traffic Shaping", "With Traffic Shaping using HTB"))


gg <- ggplot()
gg <- gg + geom_point(data = data_df, mapping = aes(x = packet_seq_no, y = packet_delay_in_secs, color=flow_id), shape = 16, size = 3, alpha = 1/3)
                      #shape = 21, fill = "black", color = "black", size = 3, alpha = 1/3)
#gg <- gg + scale_shape_manual(values=c(15, 16, 16, 17, 18))
gg <- gg + scale_color_manual(values=c('#1f1f1f','#660000', '#EA9999', '#E69138', '#B4A7D6'))
gg <- gg + facet_grid(flow_id ~ label, scales = "free")
gg <- gg + coord_cartesian()
gg <- gg + xlab("Packet")
gg <- gg + ylab("Latency (sec)")
gg <- gg + ggtitle("End-to-End Delay in non-QoS vs QoS")
gg <- gg + theme(axis.text = element_text(size = 12),
                 axis.title = element_text(size = 16),
                 axis.title.y = element_text(margin = margin(t = 0, r = 20, b = 0, l = 0)),
                 axis.title.x = element_text(margin = margin(t = 20, r = 0, b = 0, l = 0)),
                 plot.title = element_text(size = 18, face = "bold", hjust = 0.5,
                                           margin = margin(t = 0, r = 0, b = 20, l = 0)),
                 strip.background = element_rect(colour = "black", fill = "white"),
                 strip.text = element_text(face = "bold", size = 9),
                 legend.position = "none" )
#gg <- scale_color_brewer(palette = "Set3")
#print(gg)

theme_get()
theme_set(theme_bw())
print(gg)

ggsave(filename = "./with_and_without_qdisc.png", units = "cm", 
       width = 29.7, height = 21, dpi = 600)


prio_df <- read.csv(file = 'data_with_qdisc.csv')

prio_df$flow_id <- factor(prio_df$flow_id, levels = c("1", "2", "3", "4", "5"), 
                          labels = c("Medical Evacuation", "Obstacle Alert", "Video", "Picture", "FFT"))

prio <- ggplot()
prio <- prio + geom_point(data = prio_df, mapping = aes(x = packet_seq_no, y = packet_delay_in_secs, color=flow_id), shape = 16, size = 3, alpha = 1/3)
#shape = 21, fill = "black", color = "black", size = 3, alpha = 1/3)
#gg <- gg + scale_shape_manual(values=c(15, 16, 16, 17, 18))
prio <- prio + scale_color_manual(values=c('#1f1f1f','#660000', '#EA9999', '#E69138', '#B4A7D6'))
prio <- prio + coord_cartesian()
prio <- prio + xlab("Packet")
prio <- prio + ylab("Latency (sec)")
prio <- prio + ggtitle("End-to-End Delay in non-QoS vs QoS")
prio <- prio + theme(axis.text = element_text(size = 12),
                 axis.title = element_text(size = 16),
                 axis.title.y = element_text(margin = margin(t = 0, r = 20, b = 0, l = 0)),
                 axis.title.x = element_text(margin = margin(t = 20, r = 0, b = 0, l = 0)),
                 plot.title = element_text(size = 18, face = "bold", hjust = 0.5,
                                           margin = margin(t = 0, r = 0, b = 20, l = 0)),
                 strip.background = element_rect(colour = "black", fill = "white"),
                 strip.text = element_text(face = "bold", size = 9),
                 legend.position = "none" )

theme_get()
theme_set(theme_bw())
print(prio)
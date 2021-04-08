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


data_df <- read.csv(file = 'data_with_prio.csv')

data_df$flow_id <- factor(data_df$flow_id, levels = c("1", "2", "3", "4", "5"), 
                          labels = c("Medical Evacuation", "Obstacle Alert", "Video", "Picture", "FFT"))

colnames(data_df)[which(names(data_df) == "flow_id")] <- "Messages"


gg <- ggplot()
gg <- gg + geom_point(data = data_df, mapping = aes(x = packet_seq_no, y = packet_delay_in_secs, color=Messages, shape=Messages),  size = 4, stroke = 1)
gg <- gg + scale_shape_manual(values=c(4, 4, 4, 4, 4))
gg <- gg + scale_color_manual(values=c('gray0','firebrick3', 'lightgoldenrod', 'lightslategray', 'sandybrown'))
gg <- gg + coord_cartesian()
gg <- gg + xlab("Packet")
gg <- gg + ylab("Latency (sec)")
gg <- gg + ggtitle("End-to-End Delay with Traffic shaping and prioritization")

gg <- gg + theme(axis.text = element_text(size = 12),
                 axis.title = element_text(size = 16),
                 axis.title.y = element_text(margin = margin(t = 0, r = 20, b = 0, l = 0)),
                 axis.title.x = element_text(margin = margin(t = 20, r = 0, b = 0, l = 0)),
                 plot.title = element_text(size = 18, face = "bold", hjust = 0.5,
                                           margin = margin(t = 0, r = 0, b = 20, l = 0)),
                 strip.background = element_rect(colour = "black", fill = "white"),
                 strip.text = element_text(face = "bold", size = 9),
                 legend.position = "right",
                 legend.title = element_text(size = 12, face = "bold", colour = "black") # legend title
                 )


gg <- gg + scale_fill_discrete(name = "Dose", labels = c("A", "B", "C", "D", "E")) 
#gg <- scale_color_brewer(palette = "Set3")
#print(gg)

theme_get()
theme_set(theme_bw())
print(gg)

ggsave(filename = "./with_prio.png", units = "cm", 
       width = 29.7, height = 21, dpi = 600)


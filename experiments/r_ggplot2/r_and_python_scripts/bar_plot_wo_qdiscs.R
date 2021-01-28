rm(list = ls())
graphics.off()

library(ggplot2)
library(dplyr)
library(RColorBrewer)
library(wesanderson)
library(pcr)
#brewer.pal.info
#display.brewer.all()
#display.brewer.all(type="seq")
#display.brewer.all(type="div")
library(grid)
library(gridExtra)

data_df_vhf <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/without_qdiscs/plot_wo_qdisc_vhf_exp_3.csv')
data_df_vhf$packets_sent <- "Packets Received"
packet_seq_no <- 1:100
message <- rep("Medical Evacuation",length(packet_seq_no))
flow1_df <- data.frame(packet_seq_no = packet_seq_no, Messages = message)
message <- rep("Obstacle Alert",length(packet_seq_no))
flow2_df <- data.frame(packet_seq_no = packet_seq_no, Messages = message)
message <- rep("Picture",length(packet_seq_no))
flow3_df <- data.frame(packet_seq_no = packet_seq_no, Messages = message)
message <- rep("Chat",length(packet_seq_no))
flow4_df <- data.frame(packet_seq_no = packet_seq_no, Messages = message)
message <- rep("FFT",length(packet_seq_no))
flow5_df <- data.frame(packet_seq_no = packet_seq_no, Messages = message)

flow_sent_df <- dplyr::bind_rows(flow1_df, flow2_df, flow3_df, flow4_df, flow5_df)
flow_sent_df$packets_sent <- "Total Packets"


data_df_vhf$flow_id <- factor(data_df_vhf$flow_id, levels = c("1", "2", "3", "4", "5"),
                          labels = c("Medical Evacuation", "Obstacle Alert", "Picture", "Chat", "FFT"))
colnames(data_df_vhf)[which(names(data_df_vhf) == "flow_id")] <- "Messages"

data_df_vhf <- dplyr::bind_rows(data_df_vhf, flow_sent_df)
data_df_vhf$packets_sent = factor(data_df_vhf$packets_sent, levels=c('Total Packets','Packets Received'))

gg_vhf <- ggplot(data = data_df_vhf, aes(x = Messages, y=packet_seq_no, fill=packets_sent))
gg_vhf <- gg_vhf + geom_bar(stat="identity", position=position_dodge(), width=0.5)
gg_vhf <- gg_vhf + scale_y_continuous(n.breaks = 15)
gg_vhf <- gg_vhf + scale_fill_manual(values=c('#c74d4c','#d7d2d3'))
gg_vhf <- gg_vhf + coord_cartesian(ylim = c(0,100))
x.labels <- c("Medical\n Evacuation", "Obstacle\n Alert", "Picture", "Chat", "FFT")
gg_vhf <- gg_vhf + scale_x_discrete(labels= x.labels)
gg_vhf <- gg_vhf + ggtitle("VHF")
gg_vhf <- gg_vhf + xlab("Messages")
gg_vhf <- gg_vhf + ylab("Packet")
gg_vhf <- gg_vhf + theme(plot.title = element_text(margin = margin(t = 0, r = 0, b = 15, l = 0), size = 28, hjust = 0.5),
                    axis.text.x = element_text(size = 22),
                   axis.text.y = element_text(size = 22),
                   axis.title = element_text(size = 28, face ="bold"),
                   axis.title.y = element_text(margin = margin(t = 0, r = 10, b = 0, l = 0)),
                   axis.title.x = element_blank(),
                   legend.position =  "none")

#####################################################################################################

data_df_uhf <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/without_qdiscs/plot_wo_qdisc_uhf_exp_3.csv')
data_df_uhf$packets_sent <- "Packets Received"
packet_seq_no <- 1:100
message <- rep("Medical Evacuation",length(packet_seq_no))
flow1_df <- data.frame(packet_seq_no = packet_seq_no, Messages = message)
message <- rep("Obstacle Alert",length(packet_seq_no))
flow2_df <- data.frame(packet_seq_no = packet_seq_no, Messages = message)
message <- rep("Picture",length(packet_seq_no))
flow3_df <- data.frame(packet_seq_no = packet_seq_no, Messages = message)
message <- rep("Chat",length(packet_seq_no))
flow4_df <- data.frame(packet_seq_no = packet_seq_no, Messages = message)
message <- rep("FFT",length(packet_seq_no))
flow5_df <- data.frame(packet_seq_no = packet_seq_no, Messages = message)

flow_sent_df <- dplyr::bind_rows(flow1_df, flow2_df, flow3_df, flow4_df, flow5_df)
flow_sent_df$packets_sent <- "Total Packets"


data_df_uhf$flow_id <- factor(data_df_uhf$flow_id, levels = c("6", "7", "8", "9", "1"),
                          labels = c("Medical Evacuation", "Obstacle Alert", "Picture", "Chat", "FFT"))
colnames(data_df_uhf)[which(names(data_df_uhf) == "flow_id")] <- "Messages"

data_df_uhf <- dplyr::bind_rows(data_df_uhf, flow_sent_df)
data_df_uhf$packets_sent = factor(data_df_uhf$packets_sent, levels=c('Total Packets','Packets Received'))

gg_uhf <- ggplot(data = data_df_uhf, aes(x = Messages, y=packet_seq_no, fill=packets_sent))
gg_uhf <- gg_uhf + geom_bar(stat="identity", position=position_dodge(), width=0.5)
gg_uhf <- gg_uhf + scale_y_continuous(n.breaks = 15)
gg_uhf <- gg_uhf + scale_fill_manual(values=c('#c74d4c','#d7d2d3'))
gg_uhf <- gg_uhf + coord_cartesian(ylim = c(0,100))
x.labels <- c("Medical\n Evacuation", "Obstacle\n Alert", "Picture", "Chat", "FFT")
gg_uhf <- gg_uhf + scale_x_discrete(labels= x.labels)
gg_uhf <- gg_uhf + ggtitle("UHF")
gg_uhf <- gg_uhf + xlab("Messages")
gg_uhf <- gg_uhf + ylab("Packet")
gg_uhf <- gg_uhf + theme(plot.title = element_text(margin = margin(t = 0, r = 0, b = 15, l = 0), size = 28, hjust = 0.5),
                    axis.text.x = element_text(size = 22),
                   axis.text.y = element_text(size = 22),
                   axis.title = element_text(size = 28, face ="bold"),
                   axis.title.y = element_blank(),
                   axis.title.x = element_blank(),
                   legend.position =  "none")

prow <- plot_grid(gg_vhf, gg_uhf, align = "h", ncol = 2, nrow = 1, rel_widths = c(1,1))
#print(prow)


legend <- get_legend(
  gg_uhf + theme(legend.position = "bottom",
                 legend.background = element_rect(fill="transparent"),
                 legend.title = element_blank(),
                 legend.text=element_text(size=23, colour = "black"))
)

plot <- plot_grid(prow, legend, ncol = 1, nrow = 2, rel_heights = c(1, 0.1))


x.grob <- textGrob("Messages", gp=gpar(fontface="bold", col="black", fontsize=28))
grid <- grid.arrange(arrangeGrob(plot, bottom = x.grob))
print(grid)


ggsave(filename = "C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/plots/wo_qdisc_packet_drop.png",plot=grid, device="png", units = "mm", width = 400, height = 180, dpi = 600)
ggsave(filename = "C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/plots/wo_qdisc_packet_drop.eps",plot=grid, device="eps", units = "mm", width = 400, height = 180, dpi = 600)


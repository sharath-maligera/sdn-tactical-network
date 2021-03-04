rm(list = ls())
graphics.off()

library(ggplot2)
library(dplyr)
library(RColorBrewer)
library(wesanderson)
library(pcr)
library(cowplot)
#brewer.pal.info
#display.brewer.all()
#display.brewer.all(type="seq")
#display.brewer.all(type="div")
library(grid)
library(gridExtra)

data_df_vhf <- read.csv(file = '../data/without_qdiscs/plot_wo_qdisc_vhf_exp_3.csv')
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


#####################################################################################################

data_df_uhf <- read.csv(file = '../data/without_qdiscs/plot_wo_qdisc_uhf_exp_3.csv')
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




data_df_uhf$network <- "UHF"
data_df_vhf$network <- "VHF"
data_df <- rbind(data_df_vhf,data_df_uhf)
data_df$network = factor(data_df$network, levels=c('VHF','UHF'))

gg <- ggplot(data = data_df, aes(x = Messages, y=packet_seq_no, fill=packets_sent))
gg <- gg + geom_bar(stat="identity", position=position_dodge(), width=0.5)
gg <- gg + scale_y_continuous(n.breaks = 15)
gg <- gg + scale_fill_manual(values=c('#607dab','#b5c9d5'))
gg <- gg + coord_cartesian(ylim = c(0,100))
x.labels <- c("Medical\n Evacuation", "Obstacle\n Alert", "Picture", "Chat", "FFT")
gg <- gg + scale_x_discrete(labels= x.labels)
gg <- gg + xlab("Messages")
gg <- gg + ylab("Packet")
gg <- gg + facet_wrap( ~network)
gg <- gg + guides(shape = guide_legend(override.aes = list(size = 3)))
gg <- gg + theme(legend.position = "bottom",axis.text.x = element_text(angle = 90, vjust=0.4, hjust=1),
                 axis.text=element_text(size=12),legend.background = element_rect(fill="transparent"),
                 axis.title=element_text(size=12),legend.title=element_text(size=12), 
                 legend.text=element_text(size=12),strip.text.x = element_text(size = 12),strip.text.y = element_text(size = 12),
                 strip.background = element_blank(), strip.placement = "outside")
gg <- gg + theme(legend.title=element_blank())
print(gg)

#6x4

#ggsave(filename = "../plots/wo_qdisc_packet_drop.png",plot=grid, device="png", units = "mm", width = 400, height = 180, dpi = 600)
#ggsave(filename = "../plots/wo_qdisc_packet_drop.eps",plot=grid, device="eps", units = "mm", width = 400, height = 180, dpi = 600)


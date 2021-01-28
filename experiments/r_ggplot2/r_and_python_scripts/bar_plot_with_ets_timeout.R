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

data_df_0_6 <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/with_shaping_and_ets_scheduling_with_timeout/plot_ets_qdisc_0_6_kbps.csv')
data_df_0_6$packets_sent <- "Packets Received"
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


data_df_0_6$flow_id <- factor(data_df_0_6$flow_id, levels = c("1", "2", "3", "4", "5"),
                          labels = c("Medical Evacuation", "Obstacle Alert", "Picture", "Chat", "FFT"))
colnames(data_df_0_6)[which(names(data_df_0_6) == "flow_id")] <- "Messages"

data_df_0_6 <- dplyr::bind_rows(data_df_0_6, flow_sent_df)
data_df_0_6$packets_sent = factor(data_df_0_6$packets_sent, levels=c('Total Packets','Packets Received'))

gg1 <- ggplot(data = data_df_0_6, aes(x = Messages, y=packet_seq_no, fill=packets_sent))
gg1 <- gg1 + geom_bar(stat="identity", position=position_dodge(), width=0.5)
gg1 <- gg1 + scale_y_continuous(n.breaks = 15)
gg1 <- gg1 + scale_fill_manual(values=c('#607dab','#b5c9d5'))
gg1 <- gg1 + coord_cartesian(ylim = c(0,100))
x.labels <- c("Chat", "FFT", "Medical\n Evacuation", "Obstacle\n Alert", "Picture")
gg1 <- gg1 + scale_x_discrete(labels= x.labels)
gg1 <- gg1 + ggtitle("0.6 kbps")
gg1 <- gg1 + xlab("Messages")
gg1 <- gg1 + ylab("Packet")
gg1 <- gg1 + theme(plot.title = element_text(margin = margin(t = 0, r = 0, b = 15, l = 0), size = 35, hjust = 0.5),
                   axis.text.x = element_text(size = 28, angle = 45, vjust = 0.5, hjust = 0.3),
                   axis.text.y = element_text(size = 28),
                   axis.title = element_text(size = 28, face ="bold"),
                   axis.title.y = element_text(margin = margin(t = 0, r = 10, b = 0, l = 0)),
                   axis.title.x = element_blank(),
                   legend.position =  "none")

print(gg1)
#####################################################################################################

data_df_1_2 <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/with_shaping_and_ets_scheduling_with_timeout/plot_ets_qdisc_1_2_kbps.csv')
data_df_1_2$packets_sent <- "Packets Received"

data_df_1_2$flow_id <- factor(data_df_1_2$flow_id, levels = c("1", "2", "3", "4", "5"),
                          labels = c("Medical Evacuation", "Obstacle Alert", "Picture", "Chat", "FFT"))
colnames(data_df_1_2)[which(names(data_df_1_2) == "flow_id")] <- "Messages"

data_df_1_2 <- dplyr::bind_rows(data_df_1_2, flow_sent_df)
data_df_1_2$packets_sent = factor(data_df_1_2$packets_sent, levels=c('Total Packets','Packets Received'))

gg2 <- ggplot(data = data_df_1_2, aes(x = Messages, y=packet_seq_no, fill=packets_sent))
gg2 <- gg2 + geom_bar(stat="identity", position=position_dodge(), width=0.5)
gg2 <- gg2 + scale_y_continuous(n.breaks = 15)
gg2 <- gg2 + scale_fill_manual(values=c('#607dab','#b5c9d5'))
gg2 <- gg2 + coord_cartesian(ylim = c(0,100))
x.labels <- c("Chat", "FFT", "Medical\n Evacuation", "Obstacle\n Alert", "Picture")
gg2 <- gg2 + scale_x_discrete(labels= x.labels)
gg2 <- gg2 + ggtitle("1.2 kbps")
gg2 <- gg2 + xlab("Messages")
gg2 <- gg2 + ylab("Packet")
gg2 <- gg2 + theme(plot.title = element_text(margin = margin(t = 0, r = 0, b = 15, l = 0), size = 35, hjust = 0.5),
                   axis.text.x = element_text(size = 28, angle = 45, vjust = 0.5, hjust = 0.3),
                   axis.text.y = element_text(size = 28),
                   axis.title = element_text(size = 28, face ="bold"),
                   axis.title.y = element_blank(),
                   axis.title.x = element_blank(),
                   legend.position =  "none")
########################################################################################################################

data_df_2_4 <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/with_shaping_and_ets_scheduling_with_timeout/plot_ets_qdisc_2_4_kbps.csv')
data_df_2_4$packets_sent <- "Packets Received"

data_df_2_4$flow_id <- factor(data_df_2_4$flow_id, levels = c("1", "2", "3", "4", "5"),
                          labels = c("Medical Evacuation", "Obstacle Alert", "Picture", "Chat", "FFT"))
colnames(data_df_2_4)[which(names(data_df_2_4) == "flow_id")] <- "Messages"

data_df_2_4 <- dplyr::bind_rows(data_df_2_4, flow_sent_df)
data_df_2_4$packets_sent = factor(data_df_2_4$packets_sent, levels=c('Total Packets','Packets Received'))

gg3 <- ggplot(data = data_df_2_4, aes(x = Messages, y=packet_seq_no, fill=packets_sent))
gg3 <- gg3 + geom_bar(stat="identity", position=position_dodge(), width=0.5)
gg3 <- gg3 + scale_y_continuous(n.breaks = 15)
gg3 <- gg3 + scale_fill_manual(values=c('#607dab','#b5c9d5'))
gg3 <- gg3 + coord_cartesian(ylim = c(0,100))
x.labels <- c("Chat", "FFT", "Medical\n Evacuation", "Obstacle\n Alert", "Picture")
gg3 <- gg3 + scale_x_discrete(labels= x.labels)
gg3 <- gg3 + ggtitle("2.4 kbps")
gg3 <- gg3 + xlab("Messages")
gg3 <- gg3 + ylab("Packet")
gg3 <- gg3 + theme(plot.title = element_text(margin = margin(t = 0, r = 0, b = 15, l = 0), size = 35, hjust = 0.5),
                   axis.text.x = element_text(size = 28, angle = 45, vjust = 0.5, hjust = 0.3),
                   axis.text.y = element_text(size = 28),
                   axis.title = element_text(size = 28, face ="bold"),
                   axis.title.y = element_blank(),
                   axis.title.x = element_blank(),
                   legend.position =  "none")

#######################################################################################################################

data_df_4_8 <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/with_shaping_and_ets_scheduling_with_timeout/plot_ets_qdisc_4_8_kbps.csv')
data_df_4_8$packets_sent <- "Packets Received"

data_df_4_8$flow_id <- factor(data_df_4_8$flow_id, levels = c("1", "2", "3", "4", "5"),
                          labels = c("Medical Evacuation", "Obstacle Alert", "Picture", "Chat", "FFT"))
colnames(data_df_4_8)[which(names(data_df_4_8) == "flow_id")] <- "Messages"

data_df_4_8 <- dplyr::bind_rows(data_df_4_8, flow_sent_df)
data_df_4_8$packets_sent = factor(data_df_4_8$packets_sent, levels=c('Total Packets','Packets Received'))

gg4 <- ggplot(data = data_df_4_8, aes(x = Messages, y=packet_seq_no, fill=packets_sent))
gg4 <- gg4 + geom_bar(stat="identity", position=position_dodge(), width=0.5)
gg4 <- gg4 + scale_y_continuous(n.breaks = 15)
gg4 <- gg4 + scale_fill_manual(values=c('#607dab','#b5c9d5'))
gg4 <- gg4 + coord_cartesian(ylim = c(0,100))
x.labels <- c("Chat", "FFT", "Medical\n Evacuation", "Obstacle\n Alert", "Picture")
gg4 <- gg4 + scale_x_discrete(labels= x.labels)
gg4 <- gg4 + ggtitle("4.8 kbps")
gg4 <- gg4 + xlab("Messages")
gg4 <- gg4 + ylab("Packet")
gg4 <- gg4 + theme(plot.title = element_text(margin = margin(t = 0, r = 0, b = 15, l = 0), size = 35, hjust = 0.5),
                   axis.text.x = element_text(size = 28,angle = 45, vjust = 0.5, hjust = 0.3),
                   axis.text.y = element_text(size = 28),
                   axis.title = element_text(size = 28, face ="bold"),
                   axis.title.y = element_blank(),
                   axis.title.x = element_blank(),
                   legend.position =  "none")
#############################################################################################################################

data_df_9_6 <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/with_shaping_and_ets_scheduling_with_timeout/plot_ets_qdisc_9_6_kbps.csv')
data_df_9_6$packets_sent <- "Packets Received"

data_df_9_6$flow_id <- factor(data_df_9_6$flow_id, levels = c("1", "2", "3", "4", "5"),
                          labels = c("Medical Evacuation", "Obstacle Alert", "Picture", "Chat", "FFT"))
colnames(data_df_9_6)[which(names(data_df_9_6) == "flow_id")] <- "Messages"

data_df_9_6 <- dplyr::bind_rows(data_df_9_6, flow_sent_df)
data_df_9_6$packets_sent = factor(data_df_9_6$packets_sent, levels=c('Total Packets','Packets Received'))

gg5 <- ggplot(data = data_df_9_6, aes(x = Messages, y=packet_seq_no, fill=packets_sent))
gg5 <- gg5 + geom_bar(stat="identity", position=position_dodge(), width=0.5)
gg5 <- gg5 + scale_y_continuous(n.breaks = 15)
gg5 <- gg5 + scale_fill_manual(values=c('#607dab','#b5c9d5'))
gg5 <- gg5 + coord_cartesian(ylim = c(0,100))
x.labels <- c("Chat", "FFT", "Medical\n Evacuation", "Obstacle\n Alert", "Picture")
gg5 <- gg5 + scale_x_discrete(labels= x.labels)
gg5 <- gg5 + ggtitle("9.6 kbps")
gg5 <- gg5 + xlab("Messages")
gg5 <- gg5 + ylab("Packet")
gg5 <- gg5 + theme(plot.title = element_text(margin = margin(t = 0, r = 0, b = 15, l = 0), size = 35, hjust = 0.5),
                   axis.text.x = element_text(size = 28, angle = 45, vjust = 0.5, hjust = 0.3),
                   axis.text.y = element_text(size = 28),
                   axis.title = element_text(size = 28, face ="bold"),
                   axis.title.y = element_blank(),
                   axis.title.x = element_blank(),
                   legend.position =  "none")


prow <- plot_grid(gg1, gg2, gg3, gg4, gg5, align = "hv", ncol = 5, nrow = 1, rel_heights = c(1,1), rel_widths = c(1,1))


legend <- get_legend(
  gg5 + theme(legend.position = "bottom",
                 legend.background = element_rect(fill="transparent"),
                 legend.title = element_blank(),
                 legend.text=element_text(size=28, colour = "black"))
)

plot <- plot_grid(prow, legend, ncol = 1, nrow = 2, rel_heights = c(1, 0.1))


x.grob <- textGrob("Messages", gp=gpar(fontface="bold", col="black", fontsize=28))
grid <- grid.arrange(arrangeGrob(plot, bottom = x.grob))
print(grid)


ggsave(filename = "C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/plots/with_ets_qdisc_timeout_bar_plot.png",plot=grid, device="png", units = "mm", width = 900, height = 200, dpi = 600)
ggsave(filename = "C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/plots/with_ets_qdisc_timeout_bar_plot.eps",plot=grid, device="eps", units = "mm", width = 900, height = 200, dpi = 600)


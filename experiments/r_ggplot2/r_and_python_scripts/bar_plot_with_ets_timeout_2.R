library(ggplot2)
library(dplyr)
library(RColorBrewer)
library(wesanderson)
library(pcr)
library(cowplot)
library(grid)
library(gridExtra)

data_df_0_6 <- read.csv(file = '../data/with_shaping_and_ets_scheduling_with_timeout/plot_ets_qdisc_0_6_kbps.csv')
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


#####################################################################################################

data_df_1_2 <- read.csv(file = '../data/with_shaping_and_ets_scheduling_with_timeout/plot_ets_qdisc_1_2_kbps.csv')
data_df_1_2$packets_sent <- "Packets Received"


data_df_1_2$flow_id <- factor(data_df_1_2$flow_id, levels = c("1", "2", "3", "4", "5"),
                          labels = c("Medical Evacuation", "Obstacle Alert", "Picture", "Chat", "FFT"))
colnames(data_df_1_2)[which(names(data_df_1_2) == "flow_id")] <- "Messages"

data_df_1_2 <- dplyr::bind_rows(data_df_1_2, flow_sent_df)
data_df_1_2$packets_sent = factor(data_df_1_2$packets_sent, levels=c('Total Packets','Packets Received'))


########################################################################################################################

data_df_2_4 <- read.csv(file = '../data/with_shaping_and_ets_scheduling_with_timeout/plot_ets_qdisc_2_4_kbps.csv')
data_df_2_4$packets_sent <- "Packets Received"


data_df_2_4$flow_id <- factor(data_df_2_4$flow_id, levels = c("1", "2", "3", "4", "5"),
                          labels = c("Medical Evacuation", "Obstacle Alert", "Picture", "Chat", "FFT"))
colnames(data_df_2_4)[which(names(data_df_2_4) == "flow_id")] <- "Messages"

data_df_2_4 <- dplyr::bind_rows(data_df_2_4, flow_sent_df)
data_df_2_4$packets_sent = factor(data_df_2_4$packets_sent, levels=c('Total Packets','Packets Received'))



#######################################################################################################################

data_df_4_8 <- read.csv(file = '../data/with_shaping_and_ets_scheduling_with_timeout/plot_ets_qdisc_4_8_kbps.csv')
data_df_4_8$packets_sent <- "Packets Received"


data_df_4_8$flow_id <- factor(data_df_4_8$flow_id, levels = c("1", "2", "3", "4", "5"),
                          labels = c("Medical Evacuation", "Obstacle Alert", "Picture", "Chat", "FFT"))
colnames(data_df_4_8)[which(names(data_df_4_8) == "flow_id")] <- "Messages"

data_df_4_8 <- dplyr::bind_rows(data_df_4_8, flow_sent_df)
data_df_4_8$packets_sent = factor(data_df_4_8$packets_sent, levels=c('Total Packets','Packets Received'))


#############################################################################################################################

data_df_9_6 <- read.csv(file = '../data/with_shaping_and_ets_scheduling_with_timeout/plot_ets_qdisc_9_6_kbps.csv')
data_df_9_6$packets_sent <- "Packets Received"


data_df_9_6$flow_id <- factor(data_df_9_6$flow_id, levels = c("1", "2", "3", "4", "5"),
                          labels = c("Medical Evacuation", "Obstacle Alert", "Picture", "Chat", "FFT"))
colnames(data_df_9_6)[which(names(data_df_9_6) == "flow_id")] <- "Messages"

data_df_9_6 <- dplyr::bind_rows(data_df_9_6, flow_sent_df)
data_df_9_6$packets_sent = factor(data_df_9_6$packets_sent, levels=c('Total Packets','Packets Received'))



data_df_9_6$data_rate <- "9.6 kbps"
data_df_4_8$data_rate <- "4.8 kbps"
data_df_2_4$data_rate <- "2.4 kbps"
data_df_1_2$data_rate <- "1.2 kbps"
data_df_0_6$data_rate <- "0.6 kbps"
data_df <- rbind(data_df_0_6,data_df_1_2,data_df_2_4,data_df_4_8,data_df_9_6)


gg1 <- ggplot(data = data_df, aes(x = Messages, y=packet_seq_no, fill=packets_sent))
gg1 <- gg1 + geom_bar(stat="identity", position=position_dodge(), width=0.5)
gg1 <- gg1 + scale_y_continuous(n.breaks = 15)
gg1 <- gg1 + scale_fill_manual(values=c('#607dab','#b5c9d5'))
gg1 <- gg1 + coord_cartesian(ylim = c(0,100))
x.labels <- c("Chat", "FFT", "Med.\nEvac.", "Obst.\nAlert", "Picture")
gg1 <- gg1 + scale_x_discrete(labels= x.labels)
#gg1 <- gg1 + ggtitle("0.6 kbps")
gg1 <- gg1 + xlab("Messages")
gg1 <- gg1 + ylab("Packet")
gg1 <- gg1 + facet_wrap(.~ data_rate)#, ncol = 2)
gg1 <- gg1 + guides(shape = guide_legend(override.aes = list(size = 2)))
gg1 <- gg1 + theme(legend.position = c(.85, 0.2),axis.text.x = element_text(angle = 90, vjust=0.4, hjust=1), #legend.position = c(.7, 0.1)
                 axis.text=element_text(size=12),
                 axis.title=element_text(size=12),legend.title=element_text(size=12), 
                 legend.text=element_text(size=12),strip.text.x = element_text(size = 10),
                 strip.background = element_blank(), strip.placement = "outside")

gg1 <- gg1 + theme(legend.title=element_blank())
print(gg1)

#6x4

#ggsave(filename = "../plots/with_ets_qdisc_timeout_bar_plot.png",plot=grid, device="png", units = "mm", width = 900, height = 200, dpi = 600)
#ggsave(filename = "../plots/with_ets_qdisc_timeout_bar_plot.eps",plot=grid, device="eps", units = "mm", width = 900, height = 200, dpi = 600)


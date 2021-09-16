library(ggplot2)
library(dplyr)
library(tidyr)
library(RColorBrewer)
library(wesanderson)


packet_list <- list(packet_no=seq(1, 500, by = 1))

vhf_1 <- as.data.frame(packet_list)
vhf_1$meter_id <- '11'
vhf_1$experiment <- 'Experiment 1'
vhf_1$link <- 'VHF'
vhf_1$data_rate <- '10 kbps'

vhf_2 <- as.data.frame(packet_list)
vhf_2$meter_id <- '12'
vhf_2$experiment <- 'Experiment 2'
vhf_2$link <- 'VHF'
vhf_2$data_rate <- '5 kbps'

vhf_3 <- as.data.frame(packet_list)
vhf_3$meter_id <- '13'
vhf_3$experiment <- 'Experiment 3'
vhf_3$link <- 'VHF'
vhf_3$data_rate <- '3 kbps'

vhf_4 <- as.data.frame(packet_list)
vhf_4$meter_id <- '14'
vhf_4$experiment <- 'Experiment 4'
vhf_4$link <- 'VHF'
vhf_4$data_rate <- '2 kbps'

vhf_5 <- as.data.frame(packet_list)
vhf_5$meter_id <- '15'
vhf_5$experiment <- 'Experiment 5'
vhf_5$link <- 'VHF'
vhf_5$data_rate <- '1 kbps'

df_vhf <- rbind(vhf_1,vhf_2,vhf_3,vhf_4,vhf_5)

uhf_1 <- as.data.frame(packet_list)
uhf_1$meter_id <- '6'
uhf_1$experiment <- 'Experiment 1'
uhf_1$link <- 'UHF'
uhf_1$data_rate <- '240 kbps'

uhf_2 <- as.data.frame(packet_list)
uhf_2$meter_id <- '7'
uhf_2$experiment <- 'Experiment 2'
uhf_2$link <- 'UHF'
uhf_2$data_rate <- '120 kbps'

uhf_3 <- as.data.frame(packet_list)
uhf_3$meter_id <- '8'
uhf_3$experiment <- 'Experiment 3'
uhf_3$link <- 'UHF'
uhf_3$data_rate <- '60 kbps'

uhf_4 <- as.data.frame(packet_list)
uhf_4$meter_id <- '9'
uhf_4$experiment <- 'Experiment 4'
uhf_4$link <- 'UHF'
uhf_4$data_rate <- '30 kbps'

uhf_5 <- as.data.frame(packet_list)
uhf_5$meter_id <- '10'
uhf_5$experiment <- 'Experiment 5'
uhf_5$link <- 'UHF'
uhf_5$data_rate <- '15 kbps'

df_uhf <- rbind(uhf_1,uhf_2,uhf_3,uhf_4,uhf_5)

satcom_1 <- as.data.frame(packet_list)
satcom_1$meter_id <- '1'
satcom_1$experiment <- 'Experiment 1'
satcom_1$link <- 'SatCom'
satcom_1$data_rate <- '512 kbps'

satcom_2 <- as.data.frame(packet_list)
satcom_2$meter_id <- '2'
satcom_2$experiment <- 'Experiment 2'
satcom_2$link <- 'SatCom'
satcom_2$data_rate <- '256 kbps'

satcom_3 <- as.data.frame(packet_list)
satcom_3$meter_id <- '3'
satcom_3$experiment <- 'Experiment 3'
satcom_3$link <- 'SatCom'
satcom_3$data_rate <- '128 kbps'

satcom_4 <- as.data.frame(packet_list)
satcom_4$meter_id <- '4'
satcom_4$experiment <- 'Experiment 4'
satcom_4$link <- 'SatCom'
satcom_4$data_rate <- '64 kbps'

satcom_5 <- as.data.frame(packet_list)
satcom_5$meter_id <- '5'
satcom_5$experiment <- 'Experiment 5'
satcom_5$link <- 'SatCom'
satcom_5$data_rate <- '32 kbps'

df_satcom <- rbind(satcom_1,satcom_2,satcom_3,satcom_4,satcom_5)

data_df <- rbind(df_satcom, df_uhf, df_vhf)

colnames(data_df)[which(names(data_df) == "meter_id")] <- "Meters"
colnames(data_df)[which(names(data_df) == "packet_no")] <- "packets"
colnames(data_df)[which(names(data_df) == "link")] <- "Network"




# filtering the data to plot them as bars
data_df_grouped <- data_df %>% group_by(Network,data_rate)

data_df_grouped <- data_df_grouped %>% filter(packets == max(packets)) %>%  filter(row_number()==1)
#data_df_grouped <- data_df_grouped %>% filter(packets == min(packets)) %>%  filter(row_number()==1)


#c('1','2','3','4','5','6','7','8','9','10','11','12','13','14','15') y = reorder(Meters, -packets)
data_df_grouped$Meters <- factor(data_df_grouped$Meters, levels = data_df_grouped$Meters[order(data_df_grouped$packets)])

gg <- ggplot(data = data_df_grouped, aes(x = packets, y = Meters, fill=Network))
#gg <- gg + geom_line(data = data_df, mapping = aes(x = packets, y = duration_in_secs, color=Meters, linetype=Meters))
#gg <- gg + geom_point(data = data_df, mapping = aes(x = duration_in_secs, y = packets, color=Meters, shape=Meters),
#                      size = .8, stroke=1, alpha = .8)
gg <- gg +  geom_histogram(stat="identity")
#gg <- gg + coord_cartesian(xlim=c(1,499))
#gg <- scale_shape_identity()
#gg <- gg + scale_linetype_manual(values=c("longdash", "twodash", "dashed","dotdash", "dotted", "longdash", "twodash", "dashed","dotdash", "dotted"))
#gg <- gg + scale_shape_manual(values=c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
#gg <- gg + scale_fill_manual(values=c('coral3','cadetblue4', 'tan3', 'darkgoldenrod3', 'pink3', 'lavenderblush3', 'lightsteelblue1', 'thistle1', 'mistyrose1', 'slategray2'), .8)
#gg <- gg + scale_fill_manual(values=c('coral3', 'slategray2'))
gg <- gg + scale_fill_grey(start = .6, end = .2)
gg <- gg + geom_text(aes(label = data_rate, hjust = 1.2, size=16), color = "white")
#gg <- gg + geom_label(aes(label = data_rate, hjust = 0.8))
#gg <- gg + facet_grid(Network ~ data_rate,  switch = "y")
#gg <- gg + coord_flip()
gg <- gg + facet_wrap(.~ experiment, ncol = 5,strip.position = "top")
#gg <- gg + coord_cartesian()
gg <- gg + xlab("Packet")
gg <- gg + ylab("Meters")
gg <- gg + guides(shape = guide_legend(override.aes = list(size = 3)))
gg <- gg + theme(legend.position = "bottom",axis.text.x = element_text(angle = 45, vjust = 0.7, hjust = 0.7), #legend.position = c(.7, 0.1)
                 axis.text=element_text(size=18),
                 axis.title=element_text(size=18),legend.title=element_text(size=22),
                 legend.text=element_text(size=18),strip.text.x = element_text(size = 18),
                 strip.background = element_blank(), strip.placement = "outside")
theme_get()
theme_set(theme_bw())
print(gg)

ggsave(filename = "C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/plots/meter_statistics.png",plot=last_plot(), device="png", units = "mm", width = 400, height = 180, dpi = 600)
ggsave(filename = "C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/thesis_plots/meter_statistics.eps",plot=last_plot(), device="eps", units = "mm", width = 400, height = 180, dpi = 600)

library(ggplot2)
library(dplyr)
library(tidyr)
library(RColorBrewer)
library(wesanderson)

#brewer.pal.info
#display.brewer.all()
#display.brewer.all(type="seq")
#display.brewer.all(type="div")

# fuction to rename labels in data frame columns
rename_labels <-  function(df,column,raw_names,new_names){
  
  for(i in 1:length(raw_names)){
    df[,column] <- replace(df[,column], df[,column]==raw_names[i], new_names[i])
  }
  return(df)
}

data_df_9_6 <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data_icmcis/with_shaping_and_ets_scheduling_no_timeout/plot_qdisc_log_9_6_240_kbps.csv')
#data_df_9_6$data_rate <- "1:11 = 9.6kbps\n and\n 1:12 = 240kbps"
data_df_9_6$handle <- as.character(data_df_9_6$handle)
data_df_9_6$ets_bands <- data_df_9_6$handle
data_df_9_6$ets_handle <- data_df_9_6$handle
data_df_9_6$data_rate <- rename_labels(data_df_9_6,'handle',c("11:","111:", "112:", "113:", "114:", "12:","121:", "122:", "123:", "124:"),
                                       c(rep("9.6 kbps",5),rep("240 kbps",5)))$handle

data_df_4_8 <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data_icmcis/with_shaping_and_ets_scheduling_no_timeout/plot_qdisc_log_4_8_120_kbps.csv')
#data_df_4_8$data_rate <- "1:11 = 4.8kbps\n and\n 1:12 = 120kbps"
data_df_4_8$handle <- as.character(data_df_4_8$handle)
data_df_4_8$ets_bands <- data_df_4_8$handle
data_df_4_8$ets_handle <- data_df_4_8$handle
data_df_4_8$data_rate <- rename_labels(data_df_4_8,'handle',c("11:","111:", "112:", "113:", "114:", "12:","121:", "122:", "123:", "124:"),
                                       c(rep("4.8 kbps",5),rep("120 kbps",5)))$handle


data_df_2_4 <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data_icmcis/with_shaping_and_ets_scheduling_no_timeout/plot_qdisc_log_2_4_60_kbps.csv')
#data_df_2_4$data_rate <- "1:11 = 2.4kbps\n and\n 1:12 = 60kbps"
data_df_2_4$handle <- as.character(data_df_2_4$handle)
data_df_2_4$ets_bands <- data_df_2_4$handle
data_df_2_4$ets_handle <- data_df_2_4$handle
data_df_2_4$data_rate <- rename_labels(data_df_2_4,'handle',c("11:","111:", "112:", "113:", "114:", "12:","121:", "122:", "123:", "124:"),
                                       c(rep("2.4 kbps",5),rep("60 kbps",5)))$handle


data_df_1_2 <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data_icmcis/with_shaping_and_ets_scheduling_no_timeout/plot_qdisc_log_1_2_30_kbps.csv')
#data_df_1_2$data_rate <- "1:11 = 1.2kbps\n and\n 1:12 = 30kbps"
data_df_1_2$handle <- as.character(data_df_1_2$handle)
data_df_1_2$ets_bands <- data_df_1_2$handle
data_df_1_2$ets_handle <- data_df_1_2$handle
data_df_1_2$data_rate <- rename_labels(data_df_1_2,'handle',c("11:","111:", "112:", "113:", "114:", "12:","121:", "122:", "123:", "124:"),
                                       c(rep("1.2 kbps",5),rep("30 kbps",5)))$handle


data_df_0_6 <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data_icmcis/with_shaping_and_ets_scheduling_no_timeout/plot_qdisc_log_0_6_15_kbps.csv')
#data_df_0_6$data_rate <- "1:11 = 0.6kbps\n and\n 1:12 = 15kbps"
data_df_0_6$handle <- as.character(data_df_0_6$handle)
data_df_0_6$ets_bands <- data_df_0_6$handle
data_df_0_6$ets_handle <- data_df_0_6$handle
data_df_0_6$data_rate <- rename_labels(data_df_0_6,'handle',c("11:","111:", "112:", "113:", "114:", "12:","121:", "122:", "123:", "124:"),
                                       c(rep("0.6 kbps",5),rep("15 kbps",5)))$handle






data_df <- rbind(data_df_0_6,data_df_1_2,data_df_2_4,data_df_4_8,data_df_9_6)


data_df <- rename_labels(data_df,'ets_bands',c("111:", "112:", "113:", "114:", "121:", "122:", "123:", "124:"),
                             c("band-0", "band-1", "band-2", "band-3","band-0", "band-1", "band-2", "band-3"))

colnames(data_df)[which(names(data_df) == "ets_bands")] <- "Bands"

data_df <- rename_labels(data_df,'ets_handle',c("111:", "112:", "113:", "114:", "121:", "122:", "123:", "124:"),
                         c(rep("VHF",4),rep("UHF",4)))


#data_df %>% drop_na()
data_df <- data_df[!(data_df$handle=="1:"),]
data_df <- data_df[!(data_df$handle=="11:"),]
data_df <- data_df[!(data_df$handle=="12:"),]

data_df$data_rate <- factor(data_df$data_rate,
                            levels = c("0.6 kbps", "1.2 kbps", "2.4 kbps", "4.8 kbps", "9.6 kbps","15 kbps","30 kbps","60 kbps","120 kbps","240 kbps"))

data_df$ets_handle <- factor(data_df$ets_handle, levels = c("VHF", "UHF"))

#data_df[which(data_df$ets_handle=="VHF"),]$data_rate <- factor(data_df[which(data_df$ets_handle=="VHF"),]$data_rate, 
#                                                              levels = c("0.6kbps", "1.2kbps", "2.4kbps", "4.8kbps", "9.6kbps"))
#data_df[which(data_df$ets_handle=="UHF"),]$data_rate <- factor(data_df[which(data_df$ets_handle=="VHF"),]$data_rate, 
#                                                             levels = c("0.6kbps", "1.2kbps", "2.4kbps", "4.8kbps", "9.6kbps"))

df_sample <- data_df %>% sample_frac(0.30)

#df_VHF <- data_df[which(data_df$ets_handle=="VHF"),]
#df_UHF <- data_df[which(data_df$ets_handle=="UHF"),]



gg <- ggplot()
#gg <- gg + geom_line(data = data_df,aes(x = duration_in_secs, y = packets, color=Bands, linetype=Bands))
gg <- gg + geom_point(data = df_sample, mapping = aes(x =duration_in_secs, y = packets, color=Bands, shape=Bands), 
                      size = 0.8, stroke=1, alpha = .8)
#gg <- gg + coord_cartesian(xlim=c(0,200))
#gg <- gg + scale_linetype_manual(values=c("longdash", "twodash", "dashed","dotdash"))
#gg <- gg + scale_shape_manual(values=c(0, 1, 2, 3))
#gg <- gg + scale_color_manual(values=c('grey25','tomato4', 'tomato', 'goldenrod'))#c('#1e2240','#607dab', '#96abff', '#b5c9d5'))
gg <- gg + scale_color_manual(values=c('grey40','tomato4', 'tomato', 'goldenrod'))
#gg <- gg + scale_color_grey(start = 0.7, end = .2)
gg <- gg + facet_wrap( ets_handle ~ data_rate, nrow = 2, scales = "free_x")
gg <- gg + coord_cartesian()
gg <- gg + xlab("Time (sec)")
gg <- gg + ylab("Packet")
#gg <- gg + theme(axis.text.x = element_text(size = 26),
#                 axis.text.y = element_text(size = 24),
#                 axis.title = element_text(size = 30),
#                 axis.title.y = element_text(margin = margin(t = 0, r = 10, b = 0, l = 0)),
#                 axis.title.x = element_text(margin = margin(t = 10, r = 0, b = 0, l = 0)),
#                 strip.text = element_text(face = "bold", size = 15),
#                 legend.position =  c(0.908, 0.9),
#                 legend.background = element_rect(fill="transparent"),
#                 legend.title = element_text(size = 16, face = "bold", colour = "black"),
#                 legend.text=element_text(size=18, colour = "black"),
#                 legend.title.align = 0.5)
gg <- gg + guides(shape = guide_legend(override.aes = list(size = 3)))
gg <- gg + theme(legend.position="bottom",axis.text.x = element_text(angle = 35),
      axis.text=element_text(size=8),
      axis.title=element_text(size=8),legend.title=element_text(size=8), 
      legend.text=element_text(size=8),strip.text.x = element_text(size = 8),
      strip.background = element_blank(), strip.placement = "outside")
theme_get()
theme_set(theme_bw())
print(gg)

# dimission 7x5

#ggsave(filename = "C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/plots/ets_bands_occupancy_vhf_uhf.png",plot=last_plot(), device="png", units = "mm", width = 400, height = 200, dpi = 600)
#ggsave(filename = "C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/thesis_plots/ets_bands_occupancy_vhf_uhf.eps",plot=gg, device="eps", units = "mm", width = 400, height = 200, dpi = 600)

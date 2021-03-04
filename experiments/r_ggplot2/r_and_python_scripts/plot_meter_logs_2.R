library(ggplot2)
library(dplyr)
library(tidyr)
library(RColorBrewer)
library(wesanderson)

#brewer.pal.info
#display.brewer.all()
#display.brewer.all(type="seq")
#display.brewer.all(type="div")


data_df_9_6 <- read.csv(file = '../data/with_shaping_and_ets_scheduling_no_timeout/plot_meter_log_9_6_240_kbps.csv')
#data_df_9_6$data_rate <- "10kbps\n and\n 240kbps"
data_df_9_6$data_rate <- rename_labels(data_df_9_6,'meter_id',c(1,2,3,4,5,6,7,8,9,10),
                                       c("240 kbps","120 kbps","60 kbps","30 kbps","15 kbps","10 kbps",  "5 kbps", "3 kbps","2 kbps","1 kbps"))$meter_id
data_df_9_6$experiment <- "Experiment 1"
  

data_df_4_8 <- read.csv(file = '../data/with_shaping_and_ets_scheduling_no_timeout/plot_meter_log_4_8_120_kbps.csv')
#data_df_4_8$data_rate <- "5kbps\n and\n 120kbps"
data_df_4_8$data_rate <- rename_labels(data_df_4_8,'meter_id',c(1,2,3,4,5,6,7,8,9,10), 
                                       c("240 kbps","120 kbps","60 kbps","30 kbps","15 kbps","10 kbps",  "5 kbps", "3 kbps","2 kbps","1 kbps"))$meter_id
data_df_4_8$experiment <- "Experiment 2"


data_df_2_4 <- read.csv(file = '../data/with_shaping_and_ets_scheduling_no_timeout/plot_meter_log_2_4_60_kbps.csv')
#data_df_2_4$data_rate <- "3kbps\n and\n 60kbps"
data_df_2_4$data_rate <- rename_labels(data_df_2_4,'meter_id',c(1,2,3,4,5,6,7,8,9,10),
                                       c("240 kbps","120 kbps","60 kbps","30 kbps","15 kbps","10 kbps",  "5 kbps", "3 kbps","2 kbps","1 kbps"))$meter_id
data_df_2_4$experiment <- "Experiment 3"


data_df_1_2 <- read.csv(file = '../data/with_shaping_and_ets_scheduling_no_timeout/plot_meter_log_1_2_30_kbps.csv')
#data_df_1_2$data_rate <- "2kbps\n and\n 30kbps"
data_df_1_2$data_rate <- rename_labels(data_df_1_2,'meter_id',c(1,2,3,4,5,6,7,8,9,10),
                                       c("240 kbps","120 kbps","60 kbps","30 kbps","15 kbps","10 kbps",  "5 kbps", "3 kbps","2 kbps","1 kbps"))$meter_id
data_df_1_2$experiment <- "Experiment 4"


data_df_0_6 <- read.csv(file = '../data/with_shaping_and_ets_scheduling_no_timeout/plot_meter_log_0_6_15_kbps.csv')
#data_df_0_6$data_rate <- "1kbps\n and\n 15kbps"
data_df_0_6$data_rate <- rename_labels(data_df_0_6,'meter_id',c(1,2,3,4,5,6,7,8,9,10),
                                       c("240 kbps","120 kbps","60 kbps","30 kbps","15 kbps","10 kbps",  "5 kbps", "3 kbps","2 kbps","1 kbps"))$meter_id
data_df_0_6$experiment <- "Experiment 5"


# fuction to rename labels in data frame columns
rename_labels <-  function(df,column,raw_names,new_names){
  
  for(i in 1:length(raw_names)){
    df[,column] <- replace(df[,column], df[,column]==raw_names[i], new_names[i])
  }
  return(df)
}

data_df <- rbind(data_df_0_6,data_df_1_2,data_df_2_4,data_df_4_8,data_df_9_6)
data_df$Network <- rename_labels(data_df,'meter_id',c(1,2,3,4,5,6,7,8,9,10),
                                       c(rep("UHF",5),rep("VHF",5)))$meter_id

data_df$data_rate <- factor(data_df$data_rate,
                            #levels = c("9.6kbps", "4.8kbps", "2.4kbps","1.2kbps","0.6kbps","240kbps","120kbps","60kbps","30kbps","15kbps"))
                            levels = c("1 kbps","2 kbps","3 kbps","5 kbps","10 kbps","15 kbps","30 kbps","60 kbps","120 kbps","240 kbps"))

data_df$Network <- factor(data_df$Network, levels = c("VHF", "UHF"))


#data_df$data_rate_f = factor(data_df$data_rate, levels=c('1kbps\n and\n 15kbps','2kbps\n and\n 30kbps','3kbps\n and\n 60kbps','5kbps\n and\n 120kbps','10kbps\n and\n 240kbps'))

data_df$meter_id <- factor(data_df$meter_id, levels = c("1", "2", "3", "4", "5", "6", "7", "8", "9", "10")) 
                           #labels = c("Meter 1", "Meter 2", "Meter 3", "Meter 4", "Meter 5", "Meter 6", "Meter 7", "Meter 8", "Meter 9", "Meter 10"))

colnames(data_df)[which(names(data_df) == "meter_id")] <- "Meters"





# filtering the data to plot them as bars
data_df_grouped <- data_df %>% group_by(Network,data_rate)
data_df_grouped$duration_in_secs <- NULL
data_df_grouped <- data_df_grouped %>% filter(packets == max(packets)) %>%  filter(row_number()==1)
#data_df_grouped <- data_df_grouped %>% filter(packets == min(packets)) %>%  filter(row_number()==1)




gg <- ggplot(data = data_df_grouped, aes(x = Meters,y = packets, fill=Network))
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
gg <- gg + scale_fill_grey(start = .5, end = .3)
gg <- gg + geom_text(aes(label = data_rate, hjust = 1.2), color = "white")
#gg <- gg + geom_label(aes(label = data_rate, hjust = 0.8))
#gg <- gg + facet_grid(Network ~ data_rate,  switch = "y")
gg <- gg + coord_flip()
gg <- gg + facet_wrap(.~ experiment, ncol = 5,strip.position = "top")
#gg <- gg + coord_cartesian()
gg <- gg + xlab("Meters")
gg <- gg + ylab("Packet")
gg <- gg + guides(shape = guide_legend(override.aes = list(size = 3)))
gg <- gg + theme(legend.position = "bottom",axis.text.x = element_text(angle = 45), #legend.position = c(.7, 0.1)
                 axis.text=element_text(size=12),
                 axis.title=element_text(size=12),legend.title=element_text(size=12), 
                 legend.text=element_text(size=12),strip.text.x = element_text(size = 10),
                 strip.background = element_blank(), strip.placement = "outside")
theme_get()
theme_set(theme_bw())
print(gg)

#7x3



# gg <- ggplot(data = data_df_grouped, mapping = aes(x = Meters,y = packets, fill=Meters))
# #gg <- gg + geom_line(data = data_df, mapping = aes(x = packets, y = duration_in_secs, color=Meters, linetype=Meters))
# #gg <- gg + geom_point(data = data_df, mapping = aes(x = duration_in_secs, y = packets, color=Meters, shape=Meters), 
# #                      size = .8, stroke=1, alpha = .8)
# gg <- gg +  geom_histogram(stat="identity")
# scale_shape_identity()
# #gg <- gg + coord_cartesian(xlim=c(1,499))
# #gg <- scale_shape_identity()
# #gg <- gg + scale_linetype_manual(values=c("longdash", "twodash", "dashed","dotdash", "dotted", "longdash", "twodash", "dashed","dotdash", "dotted"))
# gg <- gg + scale_shape_manual(values=c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
# #gg <- gg + scale_fill_manual(values=c('grey25','tomato4', 'tomato', 'goldenrod', 'khaki4','grey25','tomato4', 'tomato', 'goldenrod', 'khaki4'))#c('coral3','cadetblue4', 'tan3', 'darkgoldenrod3', 'pink3', 'lavenderblush3', 'lightsteelblue1', 'thistle1', 'mistyrose1', 'slategray2'))
# gg <- gg + scale_fill_grey(start = 0.8, end = 0)
# #gg <- gg + facet_grid(experiment ~ data_rate,  switch = "y")
# gg <- gg + facet_wrap(experiment ~ data_rate, drop=TRUE, nrow = 2,strip.position = "top")
# gg <- gg + coord_cartesian()
# gg <- gg + xlab("Meters")
# gg <- gg + ylab("Packet")
# gg <- gg + guides(shape = guide_legend(override.aes = list(size = 2)))
# gg <- gg + theme(legend.position="none",axis.text.x = element_text(angle = 30),
#                  axis.text=element_text(size=12),
#                  axis.title=element_text(size=12),legend.title=element_text(size=12), 
#                  legend.text=element_text(size=12),strip.text.x = element_text(size = 10),
#                  strip.background = element_blank(), strip.placement = "outside")
# theme_get()
# theme_set(theme_bw())
# print(gg)



#7x3



#ggsave(filename = "../plots/with_meter_wo_timeout.png",plot=last_plot(), device="png", units = "mm", width = 400, height = 300, dpi = 600)
#ggsave(filename = "../plots/with_meter_wo_timeout.eps",plot=last_plot(), device="eps", units = "mm", width = 400, height = 300, dpi = 600)

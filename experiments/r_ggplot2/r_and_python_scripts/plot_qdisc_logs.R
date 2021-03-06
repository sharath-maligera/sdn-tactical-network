rm(list = ls())
graphics.off()

library(ggplot2)
library(dplyr)
library(tidyr)
library(RColorBrewer)
library(wesanderson)

#brewer.pal.info
#display.brewer.all()
#display.brewer.all(type="seq")
#display.brewer.all(type="div")


data_df_9_6 <- read.csv(file = '../data/with_shaping_and_ets_scheduling_no_timeout/plot_qdisc_log_9_6_240_kbps.csv')
data_df_9_6$data_rate <- "1:11 = 9.6kbps\n and\n 1:12 = 240kbps"
data_df_9_6$ets_bands <- data_df_9_6$handle
data_df_9_6$ets_handle <- data_df_9_6$handle

data_df_4_8 <- read.csv(file = '../data/with_shaping_and_ets_scheduling_no_timeout/plot_qdisc_log_4_8_120_kbps.csv')
data_df_4_8$data_rate <- "1:11 = 4.8kbps\n and\n 1:12 = 120kbps"
data_df_4_8$ets_bands <- data_df_4_8$handle
data_df_4_8$ets_handle <- data_df_4_8$handle

data_df_2_4 <- read.csv(file = '../data/with_shaping_and_ets_scheduling_no_timeout/plot_qdisc_log_2_4_60_kbps.csv')
data_df_2_4$data_rate <- "1:11 = 2.4kbps\n and\n 1:12 = 60kbps"
data_df_2_4$ets_bands <- data_df_2_4$handle
data_df_2_4$ets_handle <- data_df_2_4$handle

data_df_1_2 <- read.csv(file = '../data/with_shaping_and_ets_scheduling_no_timeout/plot_qdisc_log_1_2_30_kbps.csv')
data_df_1_2$data_rate <- "1:11 = 1.2kbps\n and\n 1:12 = 30kbps"
data_df_1_2$ets_bands <- data_df_1_2$handle
data_df_1_2$ets_handle <- data_df_1_2$handle

data_df_0_6 <- read.csv(file = '../data/with_shaping_and_ets_scheduling_no_timeout/plot_qdisc_log_0_6_15_kbps.csv')
data_df_0_6$data_rate <- "1:11 = 0.6kbps\n and\n 1:12 = 15kbps"
data_df_0_6$ets_bands <- data_df_0_6$handle
data_df_0_6$ets_handle <- data_df_0_6$handle


data_df <- rbind(data_df_0_6,data_df_1_2,data_df_2_4,data_df_4_8,data_df_9_6)

data_df$ets_bands <- factor(data_df$ets_bands, levels = c("111:", "112:", "113:", "114:", "121:", "122:", "123:", "124:"), 
                          labels = c("Band 1", "Band 2", "Band 3", "Band 4","Band 1", "Band 2", "Band 3", "Band 4"))
colnames(data_df)[which(names(data_df) == "ets_bands")] <- "Bands"

data_df$ets_handle <- factor(data_df$ets_handle, levels = c("111:", "112:", "113:", "114:", "121:", "122:", "123:", "124:"), 
                            labels = c("11:", "11:", "11:", "11:", "12:", "12:", "12:", "12:"))

#data_df %>% drop_na()
data_df <- data_df[!(data_df$handle=="1:"),]
data_df <- data_df[!(data_df$handle=="11:"),]
data_df <- data_df[!(data_df$handle=="12:"),]


gg <- ggplot()
gg <- gg + geom_line(data = data_df, mapping = aes(x = packets, y = duration_in_secs, color=Bands, linetype=Bands))
gg <- gg + geom_point(data = data_df, mapping = aes(x = packets, y = duration_in_secs, color=Bands, shape=Bands), size = 3, stroke=1.3, alpha = 1)
gg <- gg + coord_cartesian(xlim=c(0,200))
gg <- gg + scale_linetype_manual(values=c("longdash", "twodash", "dashed","dotdash"))
gg <- gg + scale_shape_manual(values=c(1, 2, 3, 4))
gg <- gg + scale_color_manual(values=c('#1e2240','#607dab', '#96abff', '#b5c9d5'))
gg <- gg + facet_grid( data_rate ~ ets_handle, scales = "free")
gg <- gg + coord_cartesian()
gg <- gg + xlab("Packet")
gg <- gg + ylab("Elapsed Time (sec)")
gg <- gg + theme(axis.text.x = element_text(size = 26),
                 axis.text.y = element_text(size = 24),
                 axis.title = element_text(size = 30),
                 axis.title.y = element_text(margin = margin(t = 0, r = 10, b = 0, l = 0)),
                 axis.title.x = element_text(margin = margin(t = 10, r = 0, b = 0, l = 0)),
                 strip.text = element_text(face = "bold", size = 15),
                 legend.position =  c(0.908, 0.9),
                 legend.background = element_rect(fill="transparent"),
                 legend.title = element_text(size = 16, face = "bold", colour = "black"),
                 legend.text=element_text(size=18, colour = "black"),
                 legend.title.align = 0.5)

theme_get()
theme_set(theme_bw())
print(gg)

ggsave(filename = "../plots/with_ets_qdisc_wo_timeout.png",plot=last_plot(), device="png", units = "mm", width = 400, height = 300, dpi = 600)
ggsave(filename = "../plots/with_ets_qdisc_wo_timeout.eps",plot=last_plot(), device="eps", units = "mm", width = 400, height = 300, dpi = 600)

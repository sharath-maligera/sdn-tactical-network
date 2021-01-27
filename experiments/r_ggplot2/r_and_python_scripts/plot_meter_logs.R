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


data_df_9_6 <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/with_shaping_and_ets_scheduling_no_timeout/plot_meter_log_9_6_240_kbps.csv')
data_df_9_6$data_rate <- "10kbps\n and\n 240kbps"

data_df_4_8 <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/with_shaping_and_ets_scheduling_no_timeout/plot_meter_log_4_8_120_kbps.csv')
data_df_4_8$data_rate <- "5kbps\n and\n 120kbps"

data_df_2_4 <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/with_shaping_and_ets_scheduling_no_timeout/plot_meter_log_2_4_60_kbps.csv')
data_df_2_4$data_rate <- "3kbps\n and\n 60kbps"

data_df_1_2 <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/with_shaping_and_ets_scheduling_no_timeout/plot_meter_log_1_2_30_kbps.csv')
data_df_1_2$data_rate <- "2kbps\n and\n 30kbps"

data_df_0_6 <- read.csv(file = 'C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/data/with_shaping_and_ets_scheduling_no_timeout/plot_meter_log_0_6_15_kbps.csv')
data_df_0_6$data_rate <- "1kbps\n and\n 15kbps"

data_df <- rbind(data_df_0_6,data_df_1_2,data_df_2_4,data_df_4_8,data_df_9_6)

data_df$data_rate_f = factor(data_df$data_rate, levels=c('1kbps\n and\n 15kbps','2kbps\n and\n 30kbps','3kbps\n and\n 60kbps','5kbps\n and\n 120kbps','10kbps\n and\n 240kbps'))

data_df$meter_id <- factor(data_df$meter_id, levels = c("1", "2", "3", "4", "5", "6", "7", "8", "9", "10"), 
                            labels = c("Meter 1", "Meter 2", "Meter 3", "Meter 4", "Meter 5", "Meter 6", "Meter 7", "Meter 8", "Meter 9", "Meter 10"))
colnames(data_df)[which(names(data_df) == "meter_id")] <- "Meters"

gg <- ggplot()
gg <- gg + geom_line(data = data_df, mapping = aes(x = packets, y = duration_in_secs, color=Meters, linetype=Meters))
gg <- gg + geom_point(data = data_df, mapping = aes(x = packets, y = duration_in_secs, color=Meters, shape=Meters), size = 3, stroke=1.3, alpha = 1)
scale_shape_identity()
gg <- gg + coord_cartesian(xlim=c(1,499))
#gg <- scale_shape_identity()
gg <- gg + scale_linetype_manual(values=c("longdash", "twodash", "dashed","dotdash", "dotted", "longdash", "twodash", "dashed","dotdash", "dotted"))
gg <- gg + scale_shape_manual(values=c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
gg <- gg + scale_color_manual(values=c('coral3','cadetblue4', 'tan3', 'darkgoldenrod3', 'pink3', 'lavenderblush3', 'lightsteelblue1', 'thistle1', 'mistyrose1', 'slategray2'))

gg <- gg + facet_grid( ~ data_rate_f, scales = "free")
gg <- gg + xlab("Packet")
gg <- gg + ylab("Elapsed Time (sec)")
gg <- gg + theme(axis.text.x = element_text(size = 23, angle = 45, vjust = 0.5, hjust = 0.7),
                 axis.text.y = element_text(size = 24),
                 axis.title = element_text(size = 30),
                 axis.title.y = element_text(margin = margin(t = 0, r = 10, b = 0, l = 0)),
                 axis.title.x = element_text(margin = margin(t = 10, r = 0, b = 0, l = 0)),
                 strip.text = element_text(face = "bold", size = 15),
                 legend.position =  c(0.908, 0.8),
                 legend.background = element_rect(fill="transparent"),
                 legend.title = element_text(size = 16, face = "bold", colour = "black"),
                 legend.text=element_text(size=18, colour = "black"),
                 legend.title.align = 0.5)

theme_get()
theme_set(theme_bw())
print(gg)

ggsave(filename = "C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/plots/with_meter_wo_timeout.png",plot=last_plot(), device="png", units = "mm", width = 400, height = 300, dpi = 600)
ggsave(filename = "C:/Users/Sharath/PycharmProjects/mininet-wifi/sdn-tactical-network/experiments/r_ggplot2/plots/with_meter_wo_timeout.eps",plot=last_plot(), device="eps", units = "mm", width = 400, height = 300, dpi = 600)

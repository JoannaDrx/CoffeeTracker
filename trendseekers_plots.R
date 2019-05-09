sgColorPalette= c("#84CF04", "#01B5BB", "#E50E63", "#6D7272", 
                  "#8F389E", "#DF8236", "#036B6B", "#F1BA2F", "#9F832D", 
                  "#94E804", "#01D4DB", "#FAC131", "#B0B8B8", "#F08C3A", 
                  "#FF106E", "#B948CC", "#05B5B5", "#CFAA3A", "black")

raw<-read_csv("trendseekers/TrendSeekers.csv")
names(raw)<-c("voteID", "choice", "timestamp")

raw$timestamp<-ymd_hms(raw$timestamp)
raw$timestamp<-with_tz(raw$timestamp, tzone="America/Los_Angeles")


# by hour
ggplot(data=raw) +
  geom_bar(mapping = aes(x = hour(raw$timestamp), fill = choice)) +
  scale_color_manual(values =sgColorPalette) +
  scale_fill_manual(values = sgColorPalette) +
  xlab("Hour") +
  ylab("Cups of coffee") +
  guides(fill=guide_legend(title="Coffee brand")) +
  theme_classic()

ggplot(data=raw, aes(x = hour(raw$timestamp), color = choice)) +
  geom_freqpoly(stat="bin", binwidth = 1, size=2) +
  scale_color_manual(values =sgColorPalette) +
  scale_fill_manual(values = sgColorPalette) +
  xlab("Hour") +
  ylab("Cups of coffee") +
  guides(color=guide_legend(title="Coffee brand")) +
  theme_classic()

# by weekday
ggplot(data=raw) +
  geom_bar(mapping = aes(x = wday(raw$timestamp, label = T), fill = choice)) +
  scale_color_manual(values =sgColorPalette) +
  scale_fill_manual(values = sgColorPalette) +
  xlab("Weekday") +
  ylab("Cups of coffee") +
  guides(fill=guide_legend(title="Coffee brand")) +
  theme_classic()


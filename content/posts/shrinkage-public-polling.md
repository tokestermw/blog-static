title: bla
date: 2013-08-23
tags: shrinkage, politics, r
author: Motoki Wu
summary: something witty
status: draft

## i need to put an image

![bla](|filename|/images/plot_data.svg)

df

	:::r
	pres <- read.csv("http://www.electoral-vote.com/evp2012/Pres/pres_polls.csv")

	pollster <- unlist(lapply(strsplit(as.character(pres$Pollster), "-"), 
							  function(x) paste(x[-length(x)], collapse = " ")))

	pollster[which(pollster == "Maine People Res. Ctr.")] <- "Maine Peoples Res. Ctr."

	pres$pollster <- pollster
	rm(pollster)

	date <- strptime(paste("2012", as.character(pres$Date), sep = " "), "%Y %b %d")
	pres$date <- date
	rm(date)

	library(ggplot2)

	svg("./plots/plot_data.svg", width = 8, height = 7)

	qplot(date, Dem / (Dem + GOP), geom = c("point"), data = pres, colour = I("red"), size = I(1)) +
	  scale_y_continuous(limits = c(.35, .65)) +
	  facet_wrap(~ State) + geom_hline(yintercept = .50) +
	  theme(panel.background = element_rect(fill = "transparent", colour = NA))

	dev.off()

dfd

![bla](|filename|/images/relative_rmse_1.svg)

	:::r
	cumavg <- function(date, date_x, x) {
	  len <- length(date)
	  out <- rep(0, len)
	  out_avg <- rep(0, length(date_x))
	  for (t in 1:len) {
	    m <- match(TRUE, date[t] <= date_x)
	    out[t] <- x[m]
	    out_avg[m] <- mean(x[1:m]) ## key averaging function!
	  }
	  list(out = out, out_avg = out_avg)
	}

	results <-
	  with(pres, {
	    out <- data.frame()
	    for (st in as.character(unique(State))) {
	      temp <-
	        cumavg(sort(unique(date)),
	               sort(unique(date[State == st])),
	               tapply((Dem / (Dem + GOP))[State == st],
	                      date$yday[State == st], mean))
	      now <- tapply((Dem / (Dem + GOP))[State == st],
	                    date$yday[State == st], mean)
	      out <- rbind(out, data.frame(State = st,
	                                   Date = sort(unique(date[State == st])),
	                                   out = now,
	                                   out_avg = temp$out_avg))
	    }
	    out
	  })

	## RMSE

	rmse <- with(results[results$Date != as.POSIXct("2012-11-06"), ], {
	  dates <- sort(unique(Date))
	  rmse <- matrix(0, nrow = length(dates), ncol = 2)
	  for (t in 1:length(dates)) {
	    ind <- dates[t] == Date
	    st <- State[ind]
	    out_real <- with(real[real$State %in% st, ], (Dem / (Dem + GOP)))
	    rmse[t, 1] <- sqrt(mean((out[ind] - out_real)^2))
	    rmse[t, 2] <- sqrt(mean((out_avg[ind] - out_real)^2))
	  }
	  rmse
	})

	x <- sort(unique(results$Date))
	x <- x[-length(x)]
	y <- rmse[, 2] / rowSums(rmse)

	svg("./plots/relative_rmse_1.svg", width = 7, height = 4)

	plot(x, y, type = "l", xlab = "Dates", ylab = "RMSE", col = "white",
	     main = "Relative RMSE of averaged (red) and raw (yellow) data")
	polygon(c(x, rev(x)), c(y, rep(0, length(y))), col = "red")
	polygon(c(x, rev(x)), c(y, rep(1, length(y))), col = "yellow")
	abline(h = .5, col = "black")

	dev.off()

dd

+++
title = "Grammar of Government Shutdown"
date = "2013-10-20"
tags = ["politics", "ggplot2", "r"]
draft = true
+++


[Treasury.io](https://github.com/csvsoundsystem/federal-treasury-api/wiki/Treasury.io-Data-Dictionary#wiki-table3a) scrapes data from the United States Treasury and puts it in a SQLite3 database.


The last graph I'd like to show is [similar to a stream graph](http://www.nytimes.com/interactive/2008/02/23/movies/20080223_REVENUE_GRAPHIC.html?_r=0) that shows total public debt transactions. Essentially, (```issues - redemption = net public debt```). The white line shows net public debt, while the issues and redemption values are *rebased* along the white line. This way, not only can you see that the public debt is increasing over time, you can directly compare sales and repayments of debt.

![bla](../../images/ledger_smoothed.svg)

I will have more on stream graphs later, meanwhile, code is posted below:

	## treasury.io
	## wget http://api.treasury.io/cc7znvq/47d80ae900e04f2/http/treasury_data.db
	sql <- 'select * from "t3a" where date > "2003-10-01"'
	d <- sqldf(sql, dbname = 'treasury_data.db')
	d$date <- as.Date(d$date)

	ind_issues <- match(d$date[d$item == "Total Redemptions"], d$date[d$item == "Total Issues"])

	df <- data.frame(date = d$date[d$item == "Total Redemptions"],
	                 redemption = - d$today[d$item == "Total Redemptions"],
	                 issues = d$today[d$item == "Total Issues"][ind_issues])
	df$net <- df$issues + df$redemption

	df.smooth <- apply(df[,-1], 2, function(x) lowess(x, f = .001))

	smoothie <- data.frame(date = rep(c(df$date, rev(df$date)), times = 2),
	                       values = c(df.smooth$redemption$y + df.smooth$net$y,
	                           rev(df.smooth$net$y),
	                           df.smooth$net$y,
	                           rev(df.smooth$issues$y) + rev(df.smooth$net$y)),
	                       ids = factor(c(rep("redemption", length = 2*dim(df)[1]), rep("issues", length = 2*dim(df)[1]))))

	svg("ledger_smoothed.svg", height = 7, width = 12)

	ggplot(data = smoothie, aes(x = date, y = values)) +
	  geom_polygon(aes(fill = ids)) +
	  scale_fill_brewer(palette = "Set1") +
	  geom_line(data = df, aes(x = date, y = lowess(net, f = .001)$y), size = 2, colour = I("white"), inherit.aes = FALSE) +
	  geom_line(data = df, aes(x = date, y = lowess(redemption, f = .001)$y + lowess(net, f = .001)$y), size = 1, colour = I("skyblue2"), inherit.aes = FALSE) +
	  geom_line(data = df, aes(x = date, y = lowess(issues, f = .001)$y + lowess(net, f = .001)$y), size = 1, colour = I("indianred2"), inherit.aes = FALSE) +
	  ylab("Daily Net Increase in Public Debt")

	dev.off()



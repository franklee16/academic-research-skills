# Note: All export prompts are protected with hashes #

# Check if required packages are already installed 

for(i in c("ggplot2", "metaviz", "sjPlot")){
	package_temp <- i
	if(!package_temp %in% installed.packages()) {
    install.packages(package_temp)
	}
}

library(ggplot2)
library(metaviz)
library(sjPlot)

# Default text formatting for plots #

text_settings <- 
	element_text(
		colour="black",
        size=10,
        face="bold"
    )

#  Example scatter plot #

data(iris)

scatter_plot <- 
	ggplot(
		iris, 
		aes(
			x = Sepal.Length, 
			y = Petal.Length)) +
  	geom_point(
  		size=3, 
  		shape=16) +
  	geom_smooth(
  		method=lm,  
  		linetype=1,
  		color="darkred",
  		se=FALSE, 
  		fullrange=TRUE) +
  	theme_classic() + 
	theme(
		axis.text.x = text_settings,
	    axis.text.y = text_settings,
	    axis.title.x = text_settings,
	    axis.title.y = text_settings,
		)+
	labs(
		x = "Sepal length",
		y = "Petal length")

#ggsave(
#	filename="your_path_here/scatter_plot.svg",
#	plot=scatter_plot, 
#	device="svg",
#	height=5,
#	width=5)

#  Example forest plot of Mozart effect meta-analysis #

forest_mozart <- 
	viz_forest(
		x = mozart[c(1:5, 7:9), c("d", "se")], 
		method = "DL",
		study_labels = c(
    		"Rauscher et al. (1993)",
    		"Kenealy and Monsef (1994)",
    		"Flohr et al. (1995a)",
    		"Flohr et al. (1995b)",
    		"Wells (1995)",
    		"Wilson and Brown (1997)",
    		"Rideout and Taylor (1997)",
    		"Rideout et al. (1998)"),          
		summary_label = "Summary effect", 
		xlab = "Cohen d",
		summary_col = "darkred")+
	theme(
		axis.text.y = text_settings,
        axis.text.x = text_settings,
        axis.title.x = text_settings)

#ggsave(
#	filename="your_path_here/forest_mozart.svg",
#	plot=forest_mozart, 
#	device="svg",
#	height=5,
#	width=8)

# Example forest plot of multiple linear regression model using sjPlot (Lüdecke, 2022) #

data(iris)

lm_example <- 
	lm(
		scale(Sepal.Length) ~ scale(Sepal.Width) + scale(Petal.Length) + scale(Petal.Width), 
		data = iris)

lm_example_forest <- 
	plot_model(
		lm_example, 
		type = "est") + 
	ggtitle("")+
	theme(
		axis.text.y = text_settings,
        axis.text.x = text_settings,
        axis.title.x = text_settings)

#ggsave(
#	filename="your_path_here/lm_example_forest.svg",
#	plot=lm_example_forest, 
#	device="svg",
#	height=2,
#	width=5)

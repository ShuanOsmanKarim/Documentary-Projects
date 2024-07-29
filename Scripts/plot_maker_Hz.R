library(tidyverse)
library(Fonology)
library(scales)
library(dplyr)
library(readxl)
library(ggrepel)  
library(bestNormalize)

# bark Conversion
bark_convert <- function(x) {
  z <- 13*atan(0.00076*x)+3.5*atan((x/7500)*(x/7500))
  return (z)
}
bark <- FALSE
clusters <- FALSE
paths <- FALSE

#####################################################
### This program plots means, clusters, and paths ###
### and plots them over cardinal vowels.          ###
#####################################################

# Instructions #

## Installing Packages ##

# If you need to install packages run the following code in the terminal; the
# easiest way is to uncomment the code block with Ctrl + Shift + C, then run the
# block with Ctrl + Enter for each line.

# install.packages('tidyverse')
# install.packages('Fonology')
# install.packages('scales')
# install.packages('dplyr')
# install.packages('readxl')
# install.packages('ggrepel')  
# install.packages('bestNormalize')

## Prepare the data ##

# You should have three types of data organized into three folders: 
# (1) mean vowel listings in a folder called "vowel_means" organized by vowel, 
# F1 and F2.
# (2) vowel path listings in a folder called"vowel_paths" organized by vowel
# number followed by a letter representing a point on the path, e.g., 9a, 9b, 9c,
# etc., F1 and F2
# (3) vowel clusters corresponding to multiple tokens of the same vowel in a 
# folder called "vowel_clusters" organized by a number representing the token, 
# F1 and F2.

# Each file should be labeled "cm vowel plot " followed by the ideal name of the
# plot to be produced. Titles can and should include special characters. The 
# current version of this program is looking for Excel files. However, a 
# future version should be adapted to a uniform CSV format


## Run the program ##

# #Click on the three dots in the top left-hand corner of the file navigator 
# and select your working directory. 
# # Then, click on the blue gear that reads 
# 'more.' 
# #Click 'Set As Working Directory.' 
# # Finally, run the program by clicking 'Source' or Ctrl + Shift + Enter

## Options ##

# If you would like to have the plots made with Bark instead of Hz, comment in 
# the following line with Ctrl + Shift + C
bark <- TRUE

set.seed(10)

if (bark == TRUE) {
  units <- "Bark"
  cc_xlim_h <- 15.5
  cc_xlim_l <- 5
  cc_ylim_h <- 8
  cc_ylim_l <- 2
} else {
    units <- "Hz"
    cc_xlim_h <- 2700
    cc_xlim_l <- 400
    cc_ylim_h <- 800
    cc_ylim_l <- 200
}

# upload Cardnal vowels
Cardnal_vowels <- read_csv("Cardnal_vowels.csv")
# Cardnal_vowels <- read_csv("Mean stressed long vowels.csv")

foldernames <- c("vowel_means", "vowel_paths", "vowel_clusters")

for (i in 1:length(foldernames)) {
  foldername <- foldernames[i]
  if (i == 2) {
    paths <- TRUE
  } else if (i == 3) {
    paths <- FALSE
    clusters <- TRUE
  }

  #Iterate over files
  filenames <- list.files(foldername, pattern="*.xls", full.names=TRUE)
  for (filename in filenames){
    #map file
    df <- read_excel(filename, col_types = c("text", "numeric", "numeric", "numeric", "numeric"))
    df <- na.omit(df)
    if (bark == TRUE) {
      df$barkF1 <- sapply(df$`F1 (Hz)`, bark_convert)
      df$barkF2 <- sapply(df$`F2 (Hz)`, bark_convert)
      df <- select(df, vowel =...1, F1 = barkF1, F2 = barkF2)
    } else {
      df <- select(df, vowel =...1, F1 = 'F1 (Hz)', F2 = 'F2 (Hz)')
    }
    
    if (paths == TRUE) {
      # Extract numerical part of the labels
      df$numeric_label <- as.numeric(gsub("[a-zA-Z]", "", df$vowel))
      df$text_label <- ""
      ll <- 0
      for (i in 1:length(df$numeric_label)) {
        nl <- df$numeric_label[i]
        if (ll == nl) {
          df$text_label[i] <- ""
        } else {
          df$text_label[i] <- nl
          ll <- nl
        }
      }
      
      # Sort data by numeric label and then by the original label
      df <- df %>%
        arrange(numeric_label, vowel)
    }
    
    
    #map Cardinal Vowels
    if (bark == TRUE) {
      card_vowels = tibble(vowel = Cardnal_vowels$...1,
                           F1 = Cardnal_vowels$`F1 (Hz)`,
                           F2 = Cardnal_vowels$`F2 (Hz)`)
      card_vowels$F1 <- sapply(card_vowels$F1, bark_convert)
      card_vowels$F2 <- sapply(card_vowels$F2, bark_convert)
    } else {
      card_vowels = tibble(vowel = Cardnal_vowels$...1,
                           F1 = Cardnal_vowels$`F1 (Hz)`,
                           F2 = Cardnal_vowels$`F2 (Hz)`)
    }
    
    
    # Create plot name
    plot_name <- sub(paste(foldername, "/cm vowel plot ", sep=""), "", filename)
    plot_name <- sub(".xlsx", "", plot_name)
    plot_name <- sub(".xls", "", plot_name)
    
    # Create plot from dataframe
    df_plot <- ggplot(data = df, aes(x = F2, y = F1, label = vowel))
    if (clusters == TRUE) {
      df_plot <- df_plot +
        geom_text(size = 2, fontface = "bold", alpha = .75) # repel
    } else if (paths == TRUE) {
      df_plot <- df_plot +
        geom_text_repel(aes(label = text_label), size = 2.5, fontface = "bold", nudge_y = 0.3)
    } else {
      df_plot <- df_plot +
        geom_text(size = 3, fontface = "bold", alpha = .75) # no repel
    }
    df_plot <- df_plot + scale_y_reverse(position = "right", 
                      labels = unit_format(unit = units, sep = ""),
                      breaks = waiver()) + 
      scale_x_reverse(position = "top", 
                      labels = unit_format(unit = units, sep = ""),
                      breaks = waiver()) + 
      coord_cartesian(xlim = c(cc_xlim_h, cc_xlim_l),
                      ylim = c(cc_ylim_h, cc_ylim_l)) +
      theme_classic(base_size = 15) +
      theme(legend.position = "none",
            plot.title = element_text(hjust = 0.5), 
            text = element_text(size = 13),
            panel.border = element_rect(color = "black", 
                                        fill = NA, 
                                        size = 3)) +
      theme_void()
    
    if (paths == TRUE) {
      for(num in unique(df$numeric_label)) {
        subset_data <- df %>% filter(numeric_label == num)
        if(nrow(subset_data) > 1) {
          df_plot <- df_plot +
            geom_path(data = df, aes(x = F2, y = F1, group = numeric_label), alpha = .75, color = "black", arrow = arrow(length = unit(0.2, "cm"))) 
        }
      }
    }
    
    df_grob <- ggplotGrob(df_plot)
    
    # create cardnal vowel plot
    cv_plot <- ggplot(data = card_vowels, aes(x = F2, y = F1, color = "black", label = vowel)) +
      geom_text(size = 3, alpha = 0.75, color = "black") + # label with box
      scale_y_reverse(position = "right", 
                      labels = unit_format(unit = units, sep = ""),
                      breaks = waiver()) + 
      scale_x_reverse(position = "top", 
                      labels = unit_format(unit = units, sep = ""),
                      breaks = waiver()) + 
      labs(x = "F2\n",
           y = "F1\n",
           title = plot_name) + 
      coord_cartesian(xlim = c(cc_xlim_h, cc_xlim_l),
                      ylim = c(cc_ylim_h, cc_ylim_l)) +
      theme_classic(base_size = 15) +
      theme(legend.position = "none",
            plot.title = element_text(hjust = 0.5), 
            text = element_text(size = 13),
            panel.border = element_rect(color = "black", 
                                        fill = NA, 
                                        size = 3))
    
    # Combine the two plots
    cv_plot + 
      annotation_custom(grob = df_grob) 
    
    
    ggsave(paste(units, "/", units, plot_name, ".png"))
  }

}
Results from cohort analysis: <br>
Cohort Analysis Results: <br>
shape: (4, 4) <br>

┌─────────────┬─────────────┬───────────────┬───────────┐<br>
│ bmi_range   ┆ avg_glucose ┆ patient_count ┆ avg_age   │<br>
│ ---         ┆ ---         ┆ ---           ┆ ---       │<br>
│ str         ┆ f64         ┆ u32           ┆ f64       │<br>
╞═════════════╪═════════════╪═══════════════╪═══════════╡<br>
│ Overweight  ┆ 116.373363  ┆ 1165360       ┆ 32.880893 │<br>
│ Underweight ┆ 95.195115   ┆ 26041         ┆ 23.980646 │<br>
│ Normal      ┆ 108.004737  ┆ 664064        ┆ 31.888848 │<br>
│ Obese       ┆ 126.032016  ┆ 3066409       ┆ 33.82713  │<br>
└─────────────┴─────────────┴───────────────┴───────────┘<br>

we see that people who are higher in bmi, thus with increasing stages of obesity, have higher average glucose levels. <br>
In addition, we see that in this case, more people are obese than all three other categories combined, which might show a skewed dataset. <br>
Next, we can also see that avg_age is older with increasing bmi, which makes sense because of workspace environments and other factors. <br>

the initial flow was to filter unreasonable numbers of bmi: those greater than 60 and less than 10. <br>
Then, we use the metric of <18.5 = underweight; >18.5 and <25 = normal ; <30 and >25 = overweight; >30 = obese to split values into four categories. <br>
In the end, we calculate metrics using that filter in mid for avg_glucose, patient_count, and avg_age. <br>

The benefit of using polars is that it acts like a sql network where sufficient functions built in are readily to be used. <br>
In addition, the files are smaller than the original csvs, which makes it more efficient. <br>
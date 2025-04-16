import polars as pl
import os


def analyze_patient_cohorts(input_file: str) -> pl.DataFrame:
    """
    Analyze patient cohorts based on BMI ranges.

    Args:
        input_file: Path to the input CSV file

    Returns:
        DataFrame containing cohort analysis results with columns:
        - bmi_range: The BMI range (e.g., "Underweight", "Normal", "Overweight", "Obese")
        - avg_glucose: Mean glucose level by BMI range
        - patient_count: Number of patients by BMI range
        - avg_age: Mean age by BMI range
    """
    # Check if the input file exists
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"The file {input_file} was not found.")

    # Convert CSV to Parquet for efficient processing
    parquet_file = "patients_large.parquet"
    pl.read_csv(input_file).write_parquet(parquet_file)

    # LazyFrame pipeline using streaming-compatible logic
    cohort_results = pl.scan_parquet(parquet_file).pipe(
        lambda df: df.filter((pl.col("BMI") >= 10) & (pl.col("BMI") <= 60))  # Filter BMI in valid range
    ).pipe(
        lambda df: df.select(["BMI", "Glucose", "Age"])  # Only necessary columns
    ).pipe(
        lambda df: df.with_columns(
            pl.when(pl.col("BMI") < 18.5)
            .then(pl.lit("Underweight"))
            .when(pl.col("BMI") < 25)
            .then(pl.lit("Normal"))
            .when(pl.col("BMI") < 30)
            .then(pl.lit("Overweight"))
            .otherwise(pl.lit("Obese"))
            .alias("bmi_range")
        )
    ).pipe(
        lambda df: df.group_by("bmi_range").agg([
            pl.col("Glucose").mean().alias("avg_glucose"),
            pl.len().alias("patient_count"),
            pl.col("Age").mean().alias("avg_age")
        ])
    ).collect()  # Use new streaming engine by default (no deprecated args)

    return cohort_results


def main():
    input_file = "patients_large.csv"

    try:
        results = analyze_patient_cohorts(input_file)
        print("\nCohort Analysis Summary:")
        print(results)
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()

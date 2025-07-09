Prompt for GitHub Copilot Agent: MLOps Platform Upgrade & Refinement

You are an expert MLOps engineer tasked with upgrading a mature, cloud-native machine learning pipeline built on Azure ML. I will provide the full context of the existing, working platform and then detail a set of new requirements to enhance its intelligence, stability, and user-friendliness.

Part 1: Existing Platform Architecture (Current State)

The project is a professional MLOps platform orchestrated from an Orchestrator.ipynb notebook in Azure ML Studio.

Core Workflow: The notebook successfully connects to an Azure ML Workspace using the SDK v1 (azureml.core), which is a proven and stable connection method for this environment. It then loads data directly from a registered Azure Datastore into an in-memory pandas DataFrame.

Orchestration: The notebook loops through a list of predefined "recipes." Each recipe is a dictionary specifying a unique combination of data preparation steps. The current implementation runs two basic recipes.

Modular Execution: For each recipe, the notebook calls functions from modular Python scripts:

src/prep_pipeline.py: Takes the DataFrame and applies the data cleaning and feature engineering steps defined in the recipe's flags. This already includes optional feature interactions and outlier handling.

src/train_pipeline.py: Takes the prepared data and calls the AutoML trainer.

AutoML Engine (src/automl_trainer.py): This script uses PyCaret to perform a comprehensive model search. For each recipe, it correctly runs compare_models(), performs hyperparameter tuning with tune_model(), and finalizes the best model.

Logging: All results are logged to the managed MLflow service in the Azure ML Workspace.

This entire system is working correctly, but it needs to be made more intelligent and professional.

Part 2: New Requirements (The Task)

You will implement three major upgrades:

Requirement #1: Implement a Professional MLflow Naming Convention

The current run names are not descriptive enough. You will implement a new, user-friendly, and hierarchical naming strategy.

Action: Modify the Orchestrator.ipynb notebook.

Experiment Name: The experiment name should be clean and persistent, based on the dataset and task type. Example: Titanic - Classification Experiments.

Parent Run Name: Each full execution of the notebook should create a single master run with a descriptive, timestamped name. Example: Main_Task_Run_2025-07-09_09-30-15.

Nested Recipe Run Name: Each recipe within the master run should have its own clear, descriptive nested run. Example: Sub_Task_Advanced_KNN_Imputation.

The Training_Stage run and all individual PyCaret model runs should be correctly nested under their respective recipe run.

Requirement #2: Expand the Recipe Library

To make this a true general-purpose template, you will expand the library of preprocessing recipes from 2 to 10. These recipes should test a diverse range of hypotheses about data preparation.

Action: In Orchestrator.ipynb, replace the existing PREPROCESSING_RECIPES list with the new, expanded 10-recipe library provided below. Note that this introduces new flags (scaling_strategy, feature_selection_pval) that you will implement in the next step.

PREPROCESSING_RECIPES = [
    {"name": "Recipe_01_Baseline_Mean_Imputation", "flags": {"imputation_strategy": "mean", "handle_outliers": False, "create_interactions": False, "scaling_strategy": None, "feature_selection_pval": None}},
    {"name": "Recipe_02_Baseline_Median_Imputation", "flags": {"imputation_strategy": "median", "handle_outliers": False, "create_interactions": False, "scaling_strategy": None, "feature_selection_pval": None}},
    {"name": "Recipe_03_Advanced_KNN_Imputation", "flags": {"imputation_strategy": "knn", "handle_outliers": False, "create_interactions": False, "scaling_strategy": None, "feature_selection_pval": None}},
    {"name": "Recipe_04_Advanced_Iterative_Imputation", "flags": {"imputation_strategy": "iterative", "handle_outliers": False, "create_interactions": False, "scaling_strategy": None, "feature_selection_pval": None}},
    {"name": "Recipe_05_Outlier_Handling_with_Robust_Scaling", "flags": {"imputation_strategy": "median", "handle_outliers": True, "create_interactions": False, "scaling_strategy": "robust", "feature_selection_pval": None}},
    {"name": "Recipe_06_Standard_Scaling_Only", "flags": {"imputation_strategy": "mean", "handle_outliers": False, "create_interactions": False, "scaling_strategy": "standard", "feature_selection_pval": None}},
    {"name": "Recipe_07_Feature_Interaction_Emphasis", "flags": {"imputation_strategy": "mean", "handle_outliers": False, "create_interactions": True, "scaling_strategy": "standard", "feature_selection_pval": None}},
    {"name": "Recipe_08_Statistical_Feature_Selection", "flags": {"imputation_strategy": "mean", "handle_outliers": False, "create_interactions": False, "scaling_strategy": "standard", "feature_selection_pval": 0.05}},
    {"name": "Recipe_09_KNN_with_Interactions_and_Scaling", "flags": {"imputation_strategy": "knn", "handle_outliers": True, "create_interactions": True, "scaling_strategy": "standard", "feature_selection_pval": None}},
    {"name": "Recipe_10_The_Works_Full_Power", "flags": {"imputation_strategy": "iterative", "handle_outliers": True, "create_interactions": True, "scaling_strategy": "robust", "feature_selection_pval": 0.05}}
]


Requirement #3: Implement Advanced Statistical Techniques

You will upgrade the prep_pipeline.py script to support two new, optional data processing techniques.

Action: Modify src/prep_pipeline.py.

Add Imports: Add from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, LabelEncoder and import scipy.stats as stats.

Implement Feature Scaling:

In the run_preparation function, add a new block to handle scaling.

This block must check for a new argument: if hasattr(args, 'scaling_strategy') and args.scaling_strategy is not None:.

Based on the value of args.scaling_strategy ('standard', 'minmax', or 'robust'), it must apply the correct scaler from scikit-learn to the numerical features.

Implement Statistical Feature Selection:

Create a new helper function: select_features_by_significance(X, y, pval_threshold).

This function must use scipy.stats for the statistical tests.

For numerical features vs. a categorical target, use an ANOVA F-test (scipy.stats.f_oneway).

For categorical features vs. a categorical target, create a contingency table with pd.crosstab and then use a Chi-Squared test (scipy.stats.chi2_contingency).

Drop any feature where the p-value is greater than the pval_threshold.

Log which features are being dropped.

Integrate this function into run_preparation inside a conditional block that checks for the feature_selection_pval argument. This step should occur after cleaning but before other feature engineering.

Final Acceptance Criteria:

The notebook must run from end to end without any errors.

The MLflow UI must show a single, clean experiment named Titanic - Classification Experiments.

Inside, there must be a single parent run named Main_Task_Run_[timestamp].

Inside the parent run, there must be 10 nested runs, one for each recipe, with descriptive names like Sub_Task_Recipe_01_Baseline_Mean_Imputation.

The logs for Recipe 8 and 10 must clearly show that statistical feature selection was performed and list the dropped columns.

The logs for Recipes 5, 6, 7, 9, and 10 must show that feature scaling was applied.

All 10 recipes must run the full AutoML and HPO process and log their results correctly.

The final experiment_summary.csv must be successfully generated and logged to the master run.
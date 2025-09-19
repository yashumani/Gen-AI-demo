graph TD
    A_Input[Input: Raw Dataset (CSV) & Target Column] --> S1_PrepData[Phase 1: Data Preparation (prep_pipeline.py)];

    subgraph S1_PrepData [Phase 1: Data Preparation]
        direction LR
        P_Ingest[1a. Ingest & Validate] --> P_Clean[1b. Clean & Encode];
        P_Clean --> P_DFSOpt{1c. DFS?};
        P_DFSOpt -- Yes --> P_DFS[1d. Generate DFS Features] --> P_DFSMatrix([featuretools_matrix.parquet]);
        P_DFSOpt -- No --> P_PreparedData([prepared.parquet]);
        P_DFSMatrix --> P_OutputForTrain1(Output for Training);
        P_PreparedData --> P_OutputForTrain1;
        P_Clean --> P_EDA[1e. Generate EDA Report] --> P_EDAReport([eda_report.html]);
        P_OutputForTrain1 --> P_Manifest([prep_manifest.json]);
    end

    P_OutputForTrain1 --> S2_TrainModels[Phase 2: AutoML Training & Selection (train_pipeline.py)];
    P_Manifest --> S2_TrainModels;

    subgraph S2_TrainModels [Phase 2: AutoML Training & Selection]
        direction TB
        T_Load[2a. Load Data & MODEL_CONFIG] --> T_LoopOptuna{2b. For each model in MODEL_CONFIG};
        T_LoopOptuna --> T_ScaleOpt{2c. Scale Features (if needed)};
        T_ScaleOpt --> T_Optuna[2d. Optuna Hyperparameter Tuning];
        T_Optuna --> T_MLflowTrials([MLflow: Optuna Study & Trials]);
        T_Optuna --> T_CollectOptuna[2e. Collect Best Optuna Results];
        T_CollectOptuna --> T_LoopRetrain{2f. For each best model};
        T_LoopRetrain --> T_RetrainFinal[2g. Retrain Final Model (with scaling if needed)];
        T_RetrainFinal --> T_EvalFinal[2h. Evaluate on Test Set];
        T_EvalFinal --> T_MLflowLogFinal[2i. MLflow: Log Final Model, Metrics, Scaler, Register];
        T_MLflowLogFinal --> T_SaveModelLocal([<model>_model.joblib]);
        T_MLflowLogFinal -- If Scaled --> T_SaveScalerLocal([<model>_scaler.joblib]);
        T_MLflowLogFinal --> T_SaveTrainCols([train_columns.json]);
        T_MLflowLogFinal --> T_MLflowRegistry([MLflow Model Registry]);
        T_MLflowRegistry --> T_Promote[2j. Determine Winner & Promote to Staging];
        T_Promote --> T_Leaderboard[2k. Print Leaderboard];
    end

    T_SaveModelLocal --> S3_ServeModels[Phase 3: Model Serving (model_serving_api.py)];
    T_SaveScalerLocal --> S3_ServeModels;
    T_SaveTrainCols --> S3_ServeModels;

    subgraph S3_ServeModels [Phase 3: Model Serving]
        direction TB
        Serv_Startup[3a. API Startup: Load Models, Scalers, Train Cols] --> Serv_Endpoints{3b. API Endpoints};
        Serv_Client[API Client] -- /predict (model_alias, features) --> Serv_Endpoints;
        Serv_Endpoints -- Preprocess (OHE, Align, Scale) --> Serv_Predict[3c. Predict];
        Serv_Predict --> Serv_Response([Prediction JSON]);
        Serv_Client -- /health, /available_models --> Serv_Endpoints;
    end
    
    S3_ServeModels --> S4_TestAPI[Phase 4: API Testing (test_api.py)];
    subgraph S4_TestAPI [Phase 4: API Testing]
        Test_Exec[4a. Execute Pytest Tests] --> Test_Verify[4b. Verify API Behavior];
    end

    classDef phase_gate fill:#c9c9c9,stroke:#333,stroke-width:2px,font-weight:bold;
    classDef process_step fill:#e6f3ff,stroke:#333,stroke-width:1px;
    classDef artifact_data fill:#fff2cc,stroke:#333,stroke-width:1px,rx:5px,ry:5px;
    classDef decision_point fill:#d4ffd4,stroke:#333,stroke-width:1px;
    classDef tool_log fill:#ffe6f0,stroke:#333,stroke-width:1px;

    class S1_PrepData,S2_TrainModels,S3_ServeModels,S4_TestAPI phase_gate;
    class A_Input,P_Ingest,P_Clean,P_DFS,P_EDA,T_Load,T_ScaleOpt,T_Optuna,T_CollectOptuna,T_RetrainFinal,T_EvalFinal,T_MLflowLogFinal,T_Promote,T_Leaderboard,Serv_Startup,Serv_Endpoints,Serv_Predict,Serv_Client,Test_Exec,Test_Verify process_step;
    class P_DFSMatrix,P_PreparedData,P_EDAReport,P_Manifest,T_SaveModelLocal,T_SaveScalerLocal,T_SaveTrainCols,Serv_Response artifact_data;
    class P_DFSOpt,T_LoopOptuna,T_LoopRetrain decision_point;
    class T_MLflowTrials,T_MLflowRegistry tool_log;

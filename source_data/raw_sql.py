

base_meta_q = '''
        DROP TABLE IF EXISTS _doc_data;
        CREATE TABLE _doc_data AS

        SELECT
        	id as source_datapoint_id
        	,document_id
        	,indicator_string
        	,campaign_string
        	,region_code
        FROM source_datapoint
        WHERE document_id = %s;

        DROP TABLE IF EXISTS _doc_meta_cnt;
        CREATE TABLE _doc_meta_cnt AS
        SELECT
        	*
        	,CAST(NULL AS INT) AS source_object_id
        	,CAST(-1 AS INT) as master_object_id
        	,CAST(0 AS INT) as master_object_cnt
        FROM (
        	SELECT
        		'source_indicator' as db_model
        		,indicator_string as source_string
        		,COUNT(1) AS source_object_cnt
        	FROM _doc_data
        	GROUP BY indicator_string

        	UNION ALL

        	SELECT
        		'source_campaign' as db_model
        		,campaign_string
        		,COUNT(1) AS c
        	FROM _doc_data
        	GROUP BY campaign_string

        	UNION ALL

        	SELECT
        		'source_region' as db_model
        		,region_code
        		,COUNT(1) AS c
        	FROM _doc_data
        	GROUP BY region_code
        )x
        INNER JOIN (
        	SELECT document_id
        	FROM _doc_data LIMIT 1
        )y
        ON 1=1;

        -----------------------------
        -- insert source meta data --
        -----------------------------

        ----------------
        -- indicators --
        ----------------
        INSERT INTO source_indicator
        (indicator_string, document_id,source_guid)

        SELECT dmc.source_string, dmc.document_id, dmc.source_string || '-' || dmc.document_id
        FROM _doc_meta_cnt dmc
        WHERE db_model = 'source_indicator'
        AND NOT EXISTS (
        	SELECT 1 FROM source_indicator si
        	WHERE dmc.db_model = 'source_indicator'
        	AND dmc.source_string = si.indicator_string
        );

        UPDATE _doc_meta_cnt dmc
        SET
        	source_object_id = si.id
        FROM source_indicator si
        WHERE dmc.db_model = 'source_indicator'
        AND dmc.source_string = si.indicator_string;

        -- MASTER REGION ID --
        UPDATE _doc_meta_cnt dmc
        SET
        	master_object_id = im.master_indicator_id
        FROM indicator_map im
        WHERE dmc.db_model = 'source_indicator'
        AND dmc.source_object_id = im.source_indicator_id;


        -------------
        -- REGIONS --
        -------------

        INSERT INTO source_region
        (region_code,document_id,source_guid,is_high_risk)

        SELECT dmc.source_string, dmc.document_id, dmc.source_string || '-' || dmc.document_id, 'f'
        FROM _doc_meta_cnt dmc
        WHERE db_model = 'source_region'
        AND NOT EXISTS (
        	SELECT 1 FROM source_region sr
        	WHERE dmc.db_model = 'source_region'
        	AND dmc.source_string = sr.region_code
        );

        UPDATE _doc_meta_cnt dmc
        SET
        	source_object_id = sr.id
        FROM source_region sr
        WHERE dmc.db_model = 'source_region'
        AND dmc.source_string = sr.region_code;


        -- MASTER REGION ID --
        UPDATE _doc_meta_cnt dmc
        SET
        	master_object_id = rm.master_region_id
        FROM region_map rm
        WHERE dmc.db_model = 'source_region'
        AND dmc.source_object_id = rm.source_region_id;

        -------------
        -- CAMPAIGNS --
        -------------

        INSERT INTO source_campaign
        (campaign_string,document_id,source_guid)

        SELECT dmc.source_string, dmc.document_id, dmc.source_string || '-' || dmc.document_id
        FROM _doc_meta_cnt dmc
        WHERE db_model = 'source_campaign'
        AND NOT EXISTS (
        	SELECT 1 FROM source_campaign sc
        	WHERE dmc.db_model = 'source_campaign'
        	AND dmc.source_string = sc.campaign_string
        );

        -- SOURCE CAMPAIGN ID --
        UPDATE _doc_meta_cnt dmc
        SET
        	source_object_id = sc.id
        FROM source_campaign sc
        WHERE dmc.db_model = 'source_campaign'
        AND dmc.source_string = sc.campaign_string;

        -- MASTER CAMPAIGN ID --
        UPDATE _doc_meta_cnt dmc
        SET
        	master_object_id = cm.master_campaign_id
        FROM campaign_map cm
        WHERE dmc.db_model = 'source_campaign'
        AND dmc.source_object_id = cm.source_campaign_id;

        DROP TABLE IF EXISTS _synced_datapoints;
        CREATE TEMP TABLE _synced_datapoints  as
        SELECT
        	dd.region_code
        	,dd.indicator_string
        	,dd.campaign_string
        FROM _doc_data dd
        INNER JOIN datapoint d
        ON dd.source_datapoint_id = d.source_datapoint_id;


        UPDATE _doc_meta_cnt dmc
        SET master_object_cnt = x.cnt
        FROM (
        	SELECT 'source_indicator' as db_model,indicator_string as source_string ,COUNT(1) as cnt
        	FROM _synced_datapoints
        	GROUP BY indicator_string

        	UNION ALL

        	SELECT 'source_region' as db_model,region_code, COUNT(1) as cnt
        	FROM _synced_datapoints
        	GROUP BY region_code

        	UNION ALL

        	SELECT 'source_campaign' as db_model, campaign_string, COUNT(1) as cnt
        	FROM _synced_datapoints
        	GROUP BY campaign_string
        )x
        WHERE dmc.db_model = x.db_model
        AND dmc.source_string = x.source_string;


        --- RETURN TO RAW QUERYSET -----
        SELECT
        	document_id as id
        	,db_model
        	,source_string
        	,source_object_id
        	,master_object_id
        	,master_object_cnt
        	,source_object_cnt
        FROM _doc_meta_cnt;'''

CREATE TABLE [dbo].[tweets] (
	--Storing IDs as Strings bcz of how large the ID values are. BigInt also a good option
	id NVARCHAR(100),
	author_id NVARCHAR(100),
	conversation_id NVARCHAR(100),
	[text] NVARCHAR(500),
	created_at DATETIME
)

CREATE VIEW [dbo].[vw_tweets] AS
	SELECT 
		[total_tweets] = COUNT(*) 
	FROM dbo.tweets
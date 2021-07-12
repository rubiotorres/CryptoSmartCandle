sqlCreateTable = """CREATE TABLE IF NOT EXISTS `candle_period` (
                  `Moeda` varchar(50) NOT NULL,   
                  `Periodicidade` varchar(50) NOT NULL default '',
                  `Datetime` DATETIME default NULL,
                  `Open` float default NULL,        
                  `Low` float default NULL, 
                  `High` float default NULL,        
                  `Close` float default NULL,               
                   PRIMARY KEY  (`Periodicidade`,`Moeda`,`Datetime`)
                );
"""
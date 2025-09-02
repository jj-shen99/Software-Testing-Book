package com.glide.ui.list.filteroperator;

import org.junit.AfterClass;
import org.junit.Assert;
import org.junit.ClassRule;
import org.junit.Test;
import org.junit.experimental.categories.Category;
import org.junit.runner.RunWith;

import com.snc.junit.rules.Timeout;
import com.snc.selenium.runner.GlideUiRunner;
import com.snc.test.categories.NeedFixForPaas;

/**
 *  * 'unit' tests for list filters operator 'is not one of'.
 * 
 *  * @author SERVICE-NOW\jianjun.shen  
 *   * @date 7/5/2013   
 */
@Category(NeedFixForPaas.class)
@RunWith(GlideUiRunner.class)
public class FiltersOperatorsIsNotOneOfIT extends RecordListFilterOperatorsTest {
	
	@ClassRule
	public static Timeout fClassTimeout = new Timeout(3 * 60 * 1000);
	
	@Test
	// validate filter: category is not one of request or software
	public void testFilterOperatorIsNotOneOfChoiceListString() {
		open("/incident_list.do?sysparm_query=categoryNOT%20INrequest%2Csoftware");
		int NumRecord = recordList.getNumRowsOnPage();
		
		for (int i = 0; i< NumRecord; i++) {
			String incidentCategory = recordList.getCellValue("incident", i + 1, COLUMN_NUMBER_CATEGORY);
			Assert.assertTrue(!incidentCategory.equals("Request") && !incidentCategory.equals("Software"));
		}
	}
	
	@Test
	// validate filter: impact is not one of 1 or 2.
		public void testFilterOperatorIsNotOneOfChoiceListInteger() {
			open("/incident_list.do?sysparm_query=impactNOT%20IN1%2C2");
			int NumRecord = recordList.getNumRowsOnPage();
			
			for (int i = 0; i< NumRecord; i++) {
				String Incident_Category = recordList.getCellValue("incident", i+1, COLUMN_NUMBER_IMPACT);
				Assert.assertTrue( (Incident_Category.compareTo("1 - High")!=0) && (Incident_Category.compareTo("2 - Medium")!=0) );
			}
		}
	
	@AfterClass
	public void disposeEnvironment() {
		disposeEnvironment(false);
	}
}

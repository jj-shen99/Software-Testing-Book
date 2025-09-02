package com.glide.ui.list.filteroperator;

import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;

import com.glide.util.StringUtil;
import org.junit.AfterClass;
import org.junit.Assert;
import org.junit.BeforeClass;
import org.junit.ClassRule;
import org.junit.Test;
import org.junit.experimental.categories.Category;
import org.junit.runner.RunWith;

import com.glide.script.GlideRecord;
import com.glide.sys.GlideSession;
import com.snc.junit.rules.Timeout;
import com.snc.selenium.runner.GlideUiRunner;
import com.snc.test.categories.NeedFixForPaas;

import static org.junit.Assert.assertEquals;

/**
 *  * 'unit' tests for list filters operator 'on'.
 * 
 *  * @author SERVICE-NOW\jianjun.shen  
 *   * @date 7/8/2013   
 */
@Category(NeedFixForPaas.class)
@RunWith(GlideUiRunner.class)
public class FiltersOperatorsOnIT extends RecordListFilterOperatorsTest {
	
	SimpleDateFormat dateFormatter = new SimpleDateFormat ("yyyy-MM-dd HH:mm:ss");
	
	public static int NUMBER_OF_INCIDENTS_Now = 1;
	public static int NUMBER_OF_INCIDENTS_30MinAgo = 2;
	public static int NUMBER_OF_INCIDENTS_Yesterday = 3;
	public static int NUMBER_OF_INCIDENTS_LastWeek = 7;
	public static int NUMBER_OF_INCIDENTS_LastMonth = 5;
	public static int NUMBER_OF_INCIDENTS_ThreeMonthsAgo = 6;
	public static int NUMBER_OF_INCIDENTS_LastYear = 7;
	
	public Calendar now = new GregorianCalendar();
	public Calendar now2 = new GregorianCalendar();
	
	@ClassRule
	public static Timeout fClassTimeout = new Timeout(12 * 60 * 1000);

	@BeforeClass
	public void setupData () { 
		// now is used to create the data.
		now = Calendar.getInstance(GlideSession.get().getTimeZone());
		// now2 is used to get the current time in the tests.
		now2 = Calendar.getInstance(GlideSession.get().getTimeZone());
		// to fix the timezone issue. maybe a bug in GregorianCalendar. may need to change when DST is over.
		now.add(Calendar.HOUR, 7); 
	
		// for all existing incidents, set the 'opened' to 2 years ago, so they won't interfere with most of the tests.
		Calendar aYearAgo = ((Calendar) now.clone());
		aYearAgo.add(Calendar.YEAR, -2);
		GlideRecord gr = new GlideRecord("incident");
		gr.query();
		while (gr.next()) {
			gr.setWorkflow(false);
			gr.setValue("opened_at", dateFormatter.format((aYearAgo.getTime())).toString());
			gr.update();	
		}
		
		// create various numbers of incidents with different 'opened' date-time for the tests.
		Calendar calNow = ((Calendar) now.clone());
	    String Opened_At_Now = dateFormatter.format(calNow.getTime());
	    for (int i = 0; i < NUMBER_OF_INCIDENTS_Now; i++) {
			createIncidentRecord("Opened_At_Now", "Software", "1", "2", Opened_At_Now.toString());
		}
	        
        Calendar cal30MinAgo = ((Calendar) now.clone());
        cal30MinAgo.add(Calendar.MINUTE, -30);
        String Opened_At_30MinAgo = dateFormatter.format(cal30MinAgo.getTime());
        for (int i = 0; i < NUMBER_OF_INCIDENTS_30MinAgo; i++) {
			createIncidentRecord("Opened_At_30MinAgo", "Software", "1", "2", Opened_At_30MinAgo.toString());
		}
        
        Calendar calYesteday = ((Calendar) now.clone());
        calYesteday.add(Calendar.DAY_OF_YEAR, -1);
        String Opened_At_Yesterday = dateFormatter.format(calYesteday.getTime());
        for (int i = 0; i < NUMBER_OF_INCIDENTS_Yesterday; i++) {
			createIncidentRecord("Opened_At_Yesterday", "Software", "1", "2", Opened_At_Yesterday.toString());
		}
        
        Calendar calLastWeek = ((Calendar) now.clone());
        calLastWeek.add(Calendar.WEEK_OF_YEAR, -1);
        String Opened_At_LastWeek = dateFormatter.format(calLastWeek.getTime());
        for (int i = 0; i < NUMBER_OF_INCIDENTS_LastWeek; i++) {
			createIncidentRecord("Opened_At_LastWeek", "Software", "1", "2", Opened_At_LastWeek.toString());
		}
			
        Calendar calLastMonth = ((Calendar) now.clone());
        calLastMonth.add(Calendar.MONTH, -1);
        String Opened_At_LastMonth = dateFormatter.format(calLastMonth.getTime());
        for (int i = 0; i < NUMBER_OF_INCIDENTS_LastMonth; i++) {
			createIncidentRecord("Opened_At_LastMonth", "Software", "1", "2", Opened_At_LastMonth.toString());
		}
        
        Calendar calThreeMonthsAgo = ((Calendar) now.clone());
        calThreeMonthsAgo.add(Calendar.MONTH, -3);
        if (calThreeMonthsAgo.get(Calendar.DAY_OF_MONTH) > 1)
        	calThreeMonthsAgo.add(Calendar.DAY_OF_YEAR, -1); //to count for any confusion if Feb has 28 days, like in the test for 'last 60 days'.
        String Opened_At_ThreeMonthsAgo = dateFormatter.format(calThreeMonthsAgo.getTime());
        for (int i = 0; i < NUMBER_OF_INCIDENTS_ThreeMonthsAgo; i++) {
			createIncidentRecord("Opened_At_ThreeMonthsAgo", "Software", "1", "2", Opened_At_ThreeMonthsAgo.toString());
		}
        
        Calendar calLastYear = ((Calendar) now.clone());
        calLastYear.add(Calendar.YEAR, -1);
        String Opened_At_LastYear = dateFormatter.format(calLastYear.getTime());
        for (int i = 0; i < NUMBER_OF_INCIDENTS_LastYear; i++) {
			createIncidentRecord("Opened_At_LastYear", "Software", "1", "2", Opened_At_LastYear.toString());
		}
        //field.setQuickSearch("cache.do");
        setShowListNumberOfRows(100);
	}
	  
	@Test
	// incidents opened on 'today'.
	public void testFilterOperatorOnDateTimeToday() throws Exception  {
		String query = "opened_atONToday@javascript:gs.daysAgoStart(0)@javascript:gs.daysAgoEnd(0)";
		testTableAndQuery("incident", query);
	}
	
	@Test
	// incidents opened on 'yesterday'.
	public void testFilterOperatorOnDateTimeYesterday() throws Exception  {
		String query = "opened_atONYesterday@javascript:gs.daysAgoStart(1)@javascript:gs.daysAgoEnd(1)";
		testTableAndQuery("incident", query);
	}
	
	@Test
	// incidents opened on 'last week'.
	public void testFilterOperatorOnDateTimeLastWeek() throws Exception  {
		openNavURI("incident_list.do?sysparm_query=opened_atONLast%20week%40javascript%3Ags.beginningOfLastWeek()%40javascript%3Ags.endOfLastWeek()");
		int NumRecord = recordList.getNumRowsOnPage();
		// if the current date is the 1st day of the week (Monday), then the records created yesterday is from last week: a week is from Mon to Sun.
		if (now2.get(Calendar.DAY_OF_WEEK) == Calendar.MONDAY ) {
			if (now2.get(Calendar.HOUR) == 0 && now.get(Calendar.MINUTE) < 30) {
				assertEquals(NUMBER_OF_INCIDENTS_LastWeek + NUMBER_OF_INCIDENTS_Yesterday + NUMBER_OF_INCIDENTS_30MinAgo, recordList.getListCount());
			}
			else {  assertEquals(NUMBER_OF_INCIDENTS_LastWeek + NUMBER_OF_INCIDENTS_Yesterday, recordList.getListCount()); }
		}
		else {  assertEquals(NUMBER_OF_INCIDENTS_LastWeek, NumRecord); }

		// validate the opened date is last week for the records created last week.
		for (int i = 0; i< NumRecord; i++) {
			String OpenedDateTime = recordList.getCellValue("incident", i+1, COLUMN_NUMBER_OPENED);
			Date OpenedDate = dateFormatter.parse(OpenedDateTime);
			Calendar calOpenedDate = Calendar.getInstance();
			calOpenedDate.setTime(OpenedDate);
			// since in service-now system, a week starts from Monday, while in Java Calendar, a week starts from Sunday, so the following logic.

			boolean isMonday = now2.get(Calendar.DAY_OF_WEEK) == Calendar.MONDAY;
			int weekOfYearDiff = now2.get(Calendar.WEEK_OF_YEAR) - calOpenedDate.get(Calendar.WEEK_OF_YEAR);
			Assert.assertTrue(
					(isMonday && weekOfYearDiff == 0) // this week and it is Monday
					|| weekOfYearDiff == 1 // week before
					|| weekOfYearDiff == -51 // week before but this is a new year
			);
		}
	}
	
	@Test
	// incidents opened on 'last 3 months'. note, include the current month as well, which is the current implementation.
	public void testFilterOperatorOnDateTimeLast3MOnths() throws Exception  {
		openNavURI("incident_list.do?sysparm_query=opened_atONLast%203%20months%40javascript%3Ags.monthsAgoStart(3)%40javascript%3Ags.endOfThisMonth()");
		int NumRecord = recordList.getNumRowsOnPage();
		
		assertEquals(NUMBER_OF_INCIDENTS_ThreeMonthsAgo + NUMBER_OF_INCIDENTS_LastMonth + NUMBER_OF_INCIDENTS_LastWeek +
				            NUMBER_OF_INCIDENTS_Yesterday + NUMBER_OF_INCIDENTS_30MinAgo + NUMBER_OF_INCIDENTS_Now, recordList.getListCount());
		
		for (int i = 0; i< NumRecord; i++) {
			String OpenedDateTime = recordList.getCellValue("incident", i+1, COLUMN_NUMBER_OPENED);
			Date OpenedDate = dateFormatter.parse(OpenedDateTime);
			Calendar calOpenedDate = Calendar.getInstance();
			calOpenedDate.setTime(OpenedDate);
		
			if  (now2.get(Calendar.YEAR) != calOpenedDate.get(Calendar.YEAR) ) {
				Assert.assertTrue( (12 + now2.get(Calendar.MONTH) - calOpenedDate.get(Calendar.MONTH) ) <= 3 );
			} 
			else {
				Assert.assertTrue( (now2.get(Calendar.MONTH) - calOpenedDate.get(Calendar.MONTH) ) <= 3 );
			}
		}
	}
	
	@Test
	// incidents opened on 'last 60 days'.
	public void testFilterOperatorOnDateTimeLast60Days() throws Exception  {
		openNavURI("incident_list.do?sysparm_query=opened_atONLast%2060%20days%40javascript%3Ags.daysAgoStart(60)%40javascript%3Ags.daysAgoEnd(0)");
		int NumRecord = recordList.getNumRowsOnPage();
		
		assertEquals(NUMBER_OF_INCIDENTS_LastMonth + NUMBER_OF_INCIDENTS_LastWeek +
				            NUMBER_OF_INCIDENTS_Yesterday + NUMBER_OF_INCIDENTS_30MinAgo + NUMBER_OF_INCIDENTS_Now, recordList.getListCount());
		
		for (int i = 0; i< NumRecord; i++) {
			String OpenedDateTime = recordList.getCellValue("incident", i+1, COLUMN_NUMBER_OPENED);
			Date OpenedDate = dateFormatter.parse(OpenedDateTime);
			Calendar calOpenedDate = Calendar.getInstance();
			calOpenedDate.setTime(OpenedDate);
			int numDaysinOpenedYear = calOpenedDate.getActualMaximum(Calendar.DAY_OF_YEAR);

			if  (now2.get(Calendar.YEAR) != calOpenedDate.get(Calendar.YEAR) ) {
				Assert.assertTrue( (numDaysinOpenedYear + now2.get(Calendar.DAY_OF_YEAR) - calOpenedDate.get(Calendar.DAY_OF_YEAR) ) <= 60 );
			} 
			else {
				Assert.assertTrue( (now2.get(Calendar.DAY_OF_YEAR) - calOpenedDate.get(Calendar.DAY_OF_YEAR) ) <= 60 );
			}			
		}
	}
	
	@Test
	// incidents opened on 'last quarter'.
	public void testFilterOperatorOnDateTimeLastQuarter() throws Exception  {
		openNavURI("/incident_list.do?sysparm_query=opened_atONLast%20quarter%40javascript%3Ags.quartersAgoStart(1)%40javascript%3Ags.quartersAgoEnd(1)");
		int NumRecord = recordList.getNumRowsOnPage();
		
		for (int i = 0; i< NumRecord; i++) {
			String OpenedDateTime = recordList.getCellValue("incident", i+1, COLUMN_NUMBER_OPENED);
			Date OpenedDate = dateFormatter.parse(OpenedDateTime);
			Calendar calOpenedDate = Calendar.getInstance();
			calOpenedDate.setTime(OpenedDate);

			int openedQuarter = ( calOpenedDate.get(Calendar.MONTH) / 3 ) + 1;
			int currentQuarter = ( now2.get(Calendar.MONTH) / 3 ) + 1;
			
			if  (now2.get(Calendar.YEAR) != calOpenedDate.get(Calendar.YEAR) ) {
				Assert.assertTrue( ( (4 + currentQuarter - openedQuarter) == 1) );
			} 
			else {
				Assert.assertTrue( ( (currentQuarter - openedQuarter) == 1) );
			}		
		}
	}
	
	@Test
	// incidents opened on 'last year'.
	public void testFilterOperatorOnDateTimeLastYear() throws Exception  {
		openNavURI("incident_list.do?sysparm_query=opened_atONLast%20year%40javascript%3Ags.beginningOfLastYear()%40javascript%3Ags.endOfLastYear()");
		int NumRecord = recordList.getNumRowsOnPage();
		
		for (int i = 0; i< NumRecord; i++) {
			String OpenedDateTime = recordList.getCellValue("incident", i+1, COLUMN_NUMBER_OPENED);
			Date OpenedDate = dateFormatter.parse(OpenedDateTime);
			Calendar calOpenedDate = Calendar.getInstance();
			calOpenedDate.setTime(OpenedDate);
			
			Assert.assertTrue( (now2.get(Calendar.YEAR) - calOpenedDate.get(Calendar.YEAR) == 1) );		
		}
	}

	private void testTableAndQuery(String table, String encodedQuery) {
		// approach here is to get the records from the database before and after we display the list
		// if they don't match, then we know that a threshold of this time frame may have elapsed
		// like from one day to another
		int dbRecords1;
		int dbRecords2;

		do {
			dbRecords1 = getRecordsForQuery(table, encodedQuery);
			open(String.format("/%s_list.do?sysparm_query=%s", table, StringUtil.urlEncode(encodedQuery)));
			dbRecords2 = getRecordsForQuery(table, encodedQuery);
		} while (dbRecords1 != dbRecords2);

		assertEquals(dbRecords1, recordList.getListCount());
	}

	private int getRecordsForQuery(String table, String encodedQuery) {
		GlideRecord gr = new GlideRecord(table);
		gr.addEncodedQuery(encodedQuery);
		gr.query();
		return gr.getRowCount();
	}

	@AfterClass
	public void disposeEnvironment() {
		disposeEnvironment(false);
	}
}

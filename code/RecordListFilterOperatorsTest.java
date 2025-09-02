package com.glide.ui.list.filteroperator;

import org.junit.BeforeClass;
import org.junit.ClassRule;
import org.junit.Rule;
import org.junit.experimental.categories.Category;

import com.glide.script.GlideRecord;
import com.snc.glide.it.rules.RecordCleaner;
import com.snc.glide.it.rules.Screenshot;
import com.snc.sdlc.annotations.Story;
import com.snc.selenium.core.SNCTest;
import com.snc.test.categories.NeedFixForPaas;

/**
 *  * super class for record list filter operators tests.
 *
 *  * @author SERVICE-NOW\jianjun.shen  
 *   * @date 6/24/2013  
 */
@Category(NeedFixForPaas.class)
@Story("STRY0100288")
public class RecordListFilterOperatorsTest extends SNCTest implements ListTestFilterOperatorsConstants {

	public static int FLAG_PACKAGE_LEVEL_SETUP = 0;

	@ClassRule
	public static RecordCleaner fCleaner = new RecordCleaner();

	@Rule
	public Screenshot fScreenshot = new Screenshot();

	@BeforeClass
	public void RecordListFilterOperatorsTestSetData () {
		// initialize data: set slush bucket columns, in order
		if (FLAG_PACKAGE_LEVEL_SETUP == 0) {
			field.setQuickSearch("incident.list");
			recordList.clickPersonalizeListColumns();
			pauseMe(2);
			slushBucket.addToPersonalizeListColumn("Impact");
			slushBucket.addToPersonalizeListColumn("Duration");
			slushBucket.addToPersonalizeListColumn("Opened by");
			slushBucket.addToPersonalizeListColumn("Severity");
			slushBucket.addToPersonalizeListColumn("Closed");
			slushBucket.addToPersonalizeListColumn("Active");
			slushBucket.addToPersonalizeListColumn("Knowledge");
			slushBucket.savePersonalizeListColumn();
			FLAG_PACKAGE_LEVEL_SETUP = 1;
		}
	}

	public void setIntegerItemValue(String table, String queryField, String queryValue, String setItemColumn, int setItemValue) {
		GlideRecord gr = new GlideRecord(table);
		gr.query(queryField, queryValue);
		gr.query();
		while (gr.next()) {
			gr.setValue(setItemColumn, setItemValue);
			gr.update();
		}
	}

	public int getTableTotalRowCount(String table) {
		GlideRecord gr = new GlideRecord(table);
		gr.query();
		return gr.getRowCount();
	}

	public void setShowListNumberOfRows(int rows) {
//		item.click(LEFT_CLICK_CONTEXTMENU);
//		item.click(LEFT_CLICK_CONTEXTMENU_SHOW);
//		item.click(String.format(LEFT_CLICK_CONTEXTMENU_SHOW_SUBMENU, rows));
	}

	public void createIncidentRecord(String short_desc, String category, String impact, String severity, String opened_at) {
		GlideRecord incidentRecord = new GlideRecord("incident");
		incidentRecord.setValue("short_description", short_desc);
		incidentRecord.setValue("category", category);
		incidentRecord.setValue("impact", impact);
		incidentRecord.setValue("severity", severity);
		incidentRecord.setValue("opened_at", opened_at);
		incidentRecord.insert();
		fCleaner.add(incidentRecord);
	}
}

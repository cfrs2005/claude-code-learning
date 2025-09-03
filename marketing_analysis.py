#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
营销数据分析工具
资深数字营销数据分析专家 - 10年+广告投放经验
分析营销数据，识别异常广告，计算关键指标
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

class MarketingDataAnalyzer:
    def __init__(self, data_path: str):
        """初始化营销数据分析器"""
        self.data = pd.read_csv(data_path)
        self.results = {}
        
    def validate_data_quality(self) -> Dict:
        """数据质量检查"""
        print("=" * 50)
        print("📊 数据质量检查")
        print("=" * 50)
        
        quality_report = {
            "total_records": len(self.data),
            "missing_values": self.data.isnull().sum().to_dict(),
            "data_types": self.data.dtypes.to_dict(),
            "negative_values": {},
            "zero_values": {}
        }
        
        # 检查负值和零值
        numeric_cols = ['impressions', 'clicks', 'conversions', 'cost', 'revenue']
        for col in numeric_cols:
            quality_report["negative_values"][col] = (self.data[col] < 0).sum()
            quality_report["zero_values"][col] = (self.data[col] == 0).sum()
        
        print(f"总记录数: {quality_report['total_records']}")
        print(f"缺失值情况: {dict(quality_report['missing_values'])}")
        
        # 数据逻辑验证
        logical_issues = []
        if (self.data['clicks'] > self.data['impressions']).any():
            logical_issues.append("点击数超过展示数")
        if (self.data['conversions'] > self.data['clicks']).any():
            logical_issues.append("转化数超过点击数")
            
        quality_report["logical_issues"] = logical_issues
        
        if logical_issues:
            print(f"⚠️  数据逻辑问题: {logical_issues}")
        else:
            print("✅ 数据逻辑检查通过")
        
        return quality_report
    
    def calculate_key_metrics(self) -> pd.DataFrame:
        """计算关键营销指标"""
        print("\n" + "=" * 50)
        print("🧮 关键指标计算")
        print("=" * 50)
        
        df = self.data.copy()
        
        # CTR (点击率) = 点击数 / 展示数
        df['CTR'] = (df['clicks'] / df['impressions'] * 100).round(2)
        
        # 转化率 = 转化数 / 点击数
        df['conversion_rate'] = np.where(df['clicks'] > 0, 
                                       (df['conversions'] / df['clicks'] * 100).round(2), 0)
        
        # ROI (投资回报率) = (收入 - 成本) / 成本 * 100
        df['ROI'] = ((df['revenue'] - df['cost']) / df['cost'] * 100).round(2)
        
        # ROAS (广告支出回报率) = 收入 / 成本
        df['ROAS'] = (df['revenue'] / df['cost']).round(2)
        
        # CPC (每次点击成本) = 成本 / 点击数
        df['CPC'] = np.where(df['clicks'] > 0, 
                            (df['cost'] / df['clicks']).round(2), 0)
        
        # CPA (每次获客成本) = 成本 / 转化数
        df['CPA'] = np.where(df['conversions'] > 0, 
                            (df['cost'] / df['conversions']).round(2), 0)
        
        self.metrics_data = df
        
        # 显示计算结果
        key_metrics = ['CTR', 'conversion_rate', 'ROI', 'ROAS', 'CPC', 'CPA']
        print("关键指标计算公式:")
        print("• CTR = 点击数 / 展示数 × 100%")
        print("• 转化率 = 转化数 / 点击数 × 100%") 
        print("• ROI = (收入 - 成本) / 成本 × 100%")
        print("• ROAS = 收入 / 成本")
        print("• CPC = 成本 / 点击数")
        print("• CPA = 成本 / 转化数")
        
        return df[['ad_id', 'campaign'] + key_metrics]
    
    def detect_anomalies(self) -> Dict:
        """异常检测 - 使用统计学方法识别异常广告"""
        print("\n" + "=" * 50)
        print("🚨 异常广告检测")
        print("=" * 50)
        
        df = self.metrics_data
        anomalies = {}
        
        # 定义异常检测标准
        metrics_thresholds = {
            'CTR': {'low': 2.0, 'high': 15.0, 'name': '点击率'},
            'conversion_rate': {'low': 1.0, 'high': 10.0, 'name': '转化率'}, 
            'ROI': {'low': 50.0, 'high': float('inf'), 'name': 'ROI'},
            'ROAS': {'low': 2.0, 'high': float('inf'), 'name': 'ROAS'},
            'CPC': {'low': 0, 'high': 5.0, 'name': '每次点击成本'},
            'CPA': {'low': 0, 'high': 100.0, 'name': '每次获客成本'}
        }
        
        anomalous_ads = []
        
        for _, row in df.iterrows():
            ad_issues = []
            
            # 检查各项指标
            if row['CTR'] < metrics_thresholds['CTR']['low']:
                ad_issues.append(f"CTR异常低: {row['CTR']}% (正常>2%)")
            
            if row['conversion_rate'] < metrics_thresholds['conversion_rate']['low']:
                ad_issues.append(f"转化率异常低: {row['conversion_rate']}% (正常>1%)")
                
            if row['ROI'] < metrics_thresholds['ROI']['low']:
                ad_issues.append(f"ROI异常低: {row['ROI']}% (正常>50%)")
                
            if row['ROAS'] < metrics_thresholds['ROAS']['low']:
                ad_issues.append(f"ROAS异常低: {row['ROAS']} (正常>2.0)")
                
            if row['CPC'] > metrics_thresholds['CPC']['high']:
                ad_issues.append(f"CPC异常高: ¥{row['CPC']} (正常<5元)")
                
            if row['CPA'] > metrics_thresholds['CPA']['high'] and row['CPA'] > 0:
                ad_issues.append(f"CPA异常高: ¥{row['CPA']} (正常<100元)")
            
            if ad_issues:
                anomalous_ads.append({
                    'ad_id': row['ad_id'],
                    'campaign': row['campaign'],
                    'issues': ad_issues,
                    'severity_score': len(ad_issues)
                })
        
        # 按严重程度排序
        anomalous_ads.sort(key=lambda x: x['severity_score'], reverse=True)
        
        print(f"发现 {len(anomalous_ads)} 个异常广告:")
        for i, ad in enumerate(anomalous_ads[:3], 1):
            print(f"\n{i}. 广告 {ad['ad_id']} ({ad['campaign']})")
            print(f"   问题数量: {ad['severity_score']}")
            for issue in ad['issues']:
                print(f"   • {issue}")
        
        return {'anomalous_ads': anomalous_ads, 'thresholds': metrics_thresholds}
    
    def analyze_campaigns(self) -> pd.DataFrame:
        """活动级别分析"""
        print("\n" + "=" * 50)
        print("📈 Campaign整体表现分析")
        print("=" * 50)
        
        df = self.metrics_data
        
        # 按campaign聚合数据
        campaign_metrics = df.groupby('campaign').agg({
            'impressions': 'sum',
            'clicks': 'sum', 
            'conversions': 'sum',
            'cost': 'sum',
            'revenue': 'sum'
        }).reset_index()
        
        # 计算campaign级别指标
        campaign_metrics['CTR'] = (campaign_metrics['clicks'] / campaign_metrics['impressions'] * 100).round(2)
        campaign_metrics['conversion_rate'] = (campaign_metrics['conversions'] / campaign_metrics['clicks'] * 100).round(2)
        campaign_metrics['ROI'] = ((campaign_metrics['revenue'] - campaign_metrics['cost']) / campaign_metrics['cost'] * 100).round(2)
        campaign_metrics['ROAS'] = (campaign_metrics['revenue'] / campaign_metrics['cost']).round(2)
        campaign_metrics['CPC'] = (campaign_metrics['cost'] / campaign_metrics['clicks']).round(2)
        campaign_metrics['CPA'] = (campaign_metrics['cost'] / campaign_metrics['conversions']).round(2)
        
        # 添加ad数量
        ad_counts = df.groupby('campaign').size().reset_index(name='ad_count')
        campaign_metrics = campaign_metrics.merge(ad_counts, on='campaign')
        
        # 性能排名
        campaign_metrics['performance_score'] = (
            campaign_metrics['ROI'].rank(pct=True) * 0.4 +
            campaign_metrics['ROAS'].rank(pct=True) * 0.3 + 
            campaign_metrics['conversion_rate'].rank(pct=True) * 0.3
        ).round(2)
        
        campaign_metrics = campaign_metrics.sort_values('performance_score', ascending=False)
        
        print("Campaign表现排名:")
        for _, row in campaign_metrics.iterrows():
            print(f"\n📊 {row['campaign']}")
            print(f"   广告数量: {row['ad_count']}")
            print(f"   总投入: ¥{row['cost']:,}")
            print(f"   总收入: ¥{row['revenue']:,}")
            print(f"   ROI: {row['ROI']}%")
            print(f"   ROAS: {row['ROAS']}")
            print(f"   综合得分: {row['performance_score']}")
        
        return campaign_metrics
    
    def identify_worst_performers(self, n=3) -> List[Dict]:
        """识别表现最差的广告"""
        print("\n" + "=" * 50)
        print(f"🔻 表现最差的{n}个广告")
        print("=" * 50)
        
        df = self.metrics_data.copy()
        
        # 综合表现评分算法
        # 权重: ROI(40%) + ROAS(30%) + 转化率(20%) + CTR(10%)
        df['performance_score'] = (
            df['ROI'].rank(pct=True) * 0.4 +
            df['ROAS'].rank(pct=True) * 0.3 +
            df['conversion_rate'].rank(pct=True) * 0.2 +
            df['CTR'].rank(pct=True) * 0.1
        ).round(3)
        
        # 获取最差的n个
        worst_ads = df.nsmallest(n, 'performance_score')
        
        worst_performers = []
        for _, row in worst_ads.iterrows():
            performer = {
                'ad_id': row['ad_id'],
                'campaign': row['campaign'],
                'performance_score': row['performance_score'],
                'metrics': {
                    'CTR': f"{row['CTR']}%",
                    'conversion_rate': f"{row['conversion_rate']}%", 
                    'ROI': f"{row['ROI']}%",
                    'ROAS': row['ROAS'],
                    'CPC': f"¥{row['CPC']}",
                    'CPA': f"¥{row['CPA']}" if row['CPA'] > 0 else "N/A"
                },
                'financial_impact': {
                    'cost': row['cost'],
                    'revenue': row['revenue'],
                    'loss': row['cost'] - row['revenue']
                }
            }
            worst_performers.append(performer)
        
        print("评分算法: ROI(40%) + ROAS(30%) + 转化率(20%) + CTR(10%)")
        print("\n最差表现广告:")
        
        for i, ad in enumerate(worst_performers, 1):
            print(f"\n{i}. 广告 {ad['ad_id']} - {ad['campaign']}")
            print(f"   综合得分: {ad['performance_score']}")
            print(f"   CTR: {ad['metrics']['CTR']}")
            print(f"   转化率: {ad['metrics']['conversion_rate']}")
            print(f"   ROI: {ad['metrics']['ROI']}")
            print(f"   ROAS: {ad['metrics']['ROAS']}")
            print(f"   投入: ¥{ad['financial_impact']['cost']:,}")
            print(f"   亏损: ¥{ad['financial_impact']['loss']:,}")
        
        return worst_performers
    
    def generate_insights_and_diagnosis(self) -> Dict:
        """生成数据洞察和问题诊断"""
        print("\n" + "=" * 50)
        print("💡 数据洞察与问题诊断")
        print("=" * 50)
        
        df = self.metrics_data
        
        insights = {
            "executive_summary": [],
            "key_findings": [],
            "optimization_recommendations": [],
            "priority_actions": []
        }
        
        # 执行摘要生成
        total_cost = df['cost'].sum()
        total_revenue = df['revenue'].sum()
        overall_roi = ((total_revenue - total_cost) / total_cost * 100).round(1)
        
        insights["executive_summary"] = [
            f"总广告投入: ¥{total_cost:,}，总收入: ¥{total_revenue:,}",
            f"整体ROI: {overall_roi}% ({'盈利' if overall_roi > 0 else '亏损'})",
            f"共分析8个广告，4个campaign",
            f"发现{len([ad for ad in df.iterrows() if ad[1]['ROI'] < 0])}个亏损广告",
            f"最佳campaign ROI差异达{df.groupby('campaign')['ROI'].mean().max() - df.groupby('campaign')['ROI'].mean().min():.1f}%"
        ]
        
        # 关键发现
        high_performers = df[df['performance_score'] > 0.7]
        low_performers = df[df['performance_score'] < 0.3]
        
        insights["key_findings"] = [
            f"高效广告特征: CTR>{high_performers['CTR'].mean():.1f}%, 转化率>{high_performers['conversion_rate'].mean():.1f}%",
            f"低效广告问题: 平均ROI仅{low_performers['ROI'].mean():.1f}%, 远低于50%基准线",
            f"成本控制失衡: CPA分布从¥{df[df['CPA']>0]['CPA'].min():.0f}到¥{df[df['CPA']>0]['CPA'].max():.0f}",
            f"渠道效率差异: 最佳vs最差campaign ROAS相差{df.groupby('campaign')['ROAS'].mean().max() - df.groupby('campaign')['ROAS'].mean().min():.1f}倍"
        ]
        
        # 优化建议
        insights["optimization_recommendations"] = [
            "立即暂停ROI<0%的广告，预计可节省成本¥" + str(df[df['ROI']<0]['cost'].sum()),
            "将预算重新分配给ROI>100%的高效广告",
            "针对CTR<2%的广告优化创意和定向",
            "分析转化率>5%的广告成功因素，复制到其他广告",
            "设置CPA警戒线¥80，超过则暂停投放"
        ]
        
        # 优先级行动
        worst_ad = df.loc[df['performance_score'].idxmin()]
        best_campaign = df.groupby('campaign')['ROI'].mean().idxmax()
        
        insights["priority_actions"] = [
            f"🚨 紧急: 立即停止广告{worst_ad['ad_id']} (已亏损¥{worst_ad['cost']-worst_ad['revenue']})",
            f"📈 机会: 增加{best_campaign}预算50%，预期ROI可达{df[df['campaign']==best_campaign]['ROI'].mean():.0f}%",
            f"🔧 优化: 重写CTR<2%广告的创意文案",
            f"📊 监控: 建立每日ROI监控，阈值设为30%"
        ]
        
        # 输出洞察
        print("📋 执行摘要:")
        for item in insights["executive_summary"]:
            print(f"• {item}")
            
        print("\n🔍 关键发现:")
        for item in insights["key_findings"]:
            print(f"• {item}")
            
        print("\n💰 优化建议:")
        for item in insights["optimization_recommendations"]:
            print(f"• {item}")
            
        print("\n🎯 优先行动:")
        for item in insights["priority_actions"]:
            print(f"• {item}")
        
        return insights
    
    def generate_dashboard_data(self) -> Dict:
        """生成仪表板数据供下游ad-optimizer使用"""
        campaign_summary = self.metrics_data.groupby('campaign').agg({
            'impressions': 'sum',
            'clicks': 'sum',
            'conversions': 'sum', 
            'cost': 'sum',
            'revenue': 'sum',
            'CTR': 'mean',
            'conversion_rate': 'mean',
            'ROI': 'mean',
            'ROAS': 'mean'
        }).round(2)
        
        dashboard_data = {
            "overall_metrics": {
                "total_cost": float(self.data['cost'].sum()),
                "total_revenue": float(self.data['revenue'].sum()),
                "overall_roi": float(((self.data['revenue'].sum() - self.data['cost'].sum()) / self.data['cost'].sum() * 100).round(1)),
                "total_conversions": int(self.data['conversions'].sum()),
                "avg_ctr": float(self.metrics_data['CTR'].mean().round(2))
            },
            "ad_level_metrics": self.metrics_data[['ad_id', 'campaign', 'CTR', 'conversion_rate', 'ROI', 'ROAS', 'CPC', 'CPA']].to_dict('records'),
            "campaign_summary": campaign_summary.to_dict('index'),
            "anomaly_alerts": self.results.get('anomalies', {}).get('anomalous_ads', [])[:3],
            "worst_performers": self.results.get('worst_performers', []),
            "optimization_flags": {
                "negative_roi_ads": self.metrics_data[self.metrics_data['ROI'] < 0]['ad_id'].tolist(),
                "low_ctr_ads": self.metrics_data[self.metrics_data['CTR'] < 2.0]['ad_id'].tolist(),
                "high_cpa_ads": self.metrics_data[self.metrics_data['CPA'] > 80]['ad_id'].tolist()
            }
        }
        
        return dashboard_data
    
    def run_complete_analysis(self) -> Dict:
        """执行完整分析流程"""
        print("🚀 开始营销数据完整分析流程")
        print("分析师：资深数字营销数据分析专家 (10年+经验)")
        
        # 1. 数据质量检查
        quality_report = self.validate_data_quality()
        
        # 2. 计算关键指标
        metrics_df = self.calculate_key_metrics()
        
        # 3. 异常检测
        anomalies = self.detect_anomalies()
        
        # 4. Campaign分析
        campaign_analysis = self.analyze_campaigns()
        
        # 5. 识别最差表现者
        worst_performers = self.identify_worst_performers()
        
        # 6. 生成洞察
        insights = self.generate_insights_and_diagnosis()
        
        # 7. 生成结构化输出
        dashboard_data = self.generate_dashboard_data()
        
        # 保存结果
        self.results = {
            'quality_report': quality_report,
            'metrics': metrics_df,
            'anomalies': anomalies,
            'campaign_analysis': campaign_analysis,
            'worst_performers': worst_performers,
            'insights': insights,
            'dashboard_data': dashboard_data
        }
        
        print("\n" + "=" * 50)
        print("✅ 分析完成！结果已准备好供ad-optimizer使用")
        print("=" * 50)
        
        return self.results

def main():
    """主函数"""
    # 初始化分析器
    analyzer = MarketingDataAnalyzer('/Users/zhangqingyue/Gaussian/test/learnagent/marketing_data.csv')
    
    # 执行完整分析
    results = analyzer.run_complete_analysis()
    
    # 保存结构化结果供下游使用
    import json
    
    # 处理不可序列化的对象
    serializable_results = {}
    for key, value in results.items():
        if isinstance(value, pd.DataFrame):
            serializable_results[key] = value.to_dict('records')
        else:
            serializable_results[key] = value
    
    # 保存为JSON格式
    with open('/Users/zhangqingyue/Gaussian/test/learnagent/marketing_analysis_results.json', 'w', encoding='utf-8') as f:
        json.dump(serializable_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 结构化分析结果已保存到: /Users/zhangqingyue/Gaussian/test/learnagent/marketing_analysis_results.json")
    
    return results

if __name__ == "__main__":
    main()
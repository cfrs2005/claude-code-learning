#!/usr/bin/env python3
"""
广告数据分析 - Linus式简洁实现
不搞花哨的，直接算核心指标，用数据说话
"""

import pandas as pd
import numpy as np

def analyze_ad_performance(csv_file):
    """
    分析广告数据，计算关键指标
    "Bad programmers worry about the code. Good programmers worry about data structures."
    - Linus Torvalds
    """
    # 读取数据 - 最简单直接的方式
    df = pd.read_csv(csv_file)
    
    print("=== 原始数据检查 ===")
    print(f"总共 {len(df)} 个广告")
    print(f"涉及 {df['campaign'].nunique()} 个活动")
    print()
    
    # 计算核心指标 - 没有特殊情况，就是简单的数学
    df['CTR'] = df['clicks'] / df['impressions']
    df['conversion_rate'] = df['conversions'] / df['clicks'] 
    df['ROI'] = (df['revenue'] - df['cost']) / df['cost']
    
    # 计算CPC和CPA - 虽然题目没要求，但这是基础指标
    df['CPC'] = df['cost'] / df['clicks']
    df['CPA'] = df['cost'] / df['conversions']
    
    print("=== 关键指标汇总 ===")
    print("Ad_ID  Campaign      CTR%    Conv%    ROI%     CPC    CPA     Revenue")
    print("-" * 75)
    
    for _, row in df.iterrows():
        print(f"{row['ad_id']:<6} {row['campaign']:<12} "
              f"{row['CTR']*100:>6.2f}  {row['conversion_rate']*100:>6.2f}  "
              f"{row['ROI']*100:>6.1f}   {row['CPC']:>6.1f}  {row['CPA']:>6.1f}   "
              f"{row['revenue']:>7.0f}")
    
    print()
    
    # 找出表现最差的广告
    # Linus会说：用最简单的方法，综合评分然后排序
    df['composite_score'] = (
        df['CTR'] * 0.3 +           # 点击率权重30%
        df['conversion_rate'] * 0.3 + # 转化率权重30% 
        df['ROI'] * 0.4             # ROI权重40%（最重要）
    )
    
    worst_ads = df.nsmallest(3, 'composite_score')
    
    print("=== 表现最差的3个广告 ===")
    for i, (_, ad) in enumerate(worst_ads.iterrows(), 1):
        print(f"\n{i}. 广告 {ad['ad_id']} ({ad['campaign']})")
        print(f"   CTR: {ad['CTR']*100:.2f}% (点击率)")
        print(f"   转化率: {ad['conversion_rate']*100:.2f}%")  
        print(f"   ROI: {ad['ROI']*100:.1f}%")
        print(f"   问题分析:")
        
        # 简单直接的问题诊断，不搞复杂算法
        problems = []
        if ad['CTR'] < df['CTR'].mean():
            problems.append(f"点击率低于平均值({df['CTR'].mean()*100:.2f}%)")
        if ad['conversion_rate'] < df['conversion_rate'].mean():
            problems.append(f"转化率低于平均值({df['conversion_rate'].mean()*100:.2f}%)")
        if ad['ROI'] < 0:
            problems.append("ROI为负，亏损严重")
        elif ad['ROI'] < df['ROI'].mean():
            problems.append(f"ROI低于平均值({df['ROI'].mean()*100:.1f}%)")
            
        for problem in problems:
            print(f"     - {problem}")
    
    # 活动层面分析
    print(f"\n=== 活动层面分析 ===")
    campaign_stats = df.groupby('campaign').agg({
        'impressions': 'sum',
        'clicks': 'sum', 
        'conversions': 'sum',
        'cost': 'sum',
        'revenue': 'sum'
    }).round(2)
    
    # 计算活动级别指标
    campaign_stats['CTR'] = campaign_stats['clicks'] / campaign_stats['impressions']
    campaign_stats['conversion_rate'] = campaign_stats['conversions'] / campaign_stats['clicks']
    campaign_stats['ROI'] = (campaign_stats['revenue'] - campaign_stats['cost']) / campaign_stats['cost']
    
    print("Campaign        总展示   总点击  总转化   总成本   总收入    CTR%   Conv%   ROI%")
    print("-" * 85)
    for campaign, stats in campaign_stats.iterrows():
        print(f"{campaign:<12} {stats['impressions']:>8.0f} {stats['clicks']:>8.0f} "
              f"{stats['conversions']:>7.0f} {stats['cost']:>8.0f} {stats['revenue']:>8.0f} "
              f"{stats['CTR']*100:>6.2f} {stats['conversion_rate']*100:>6.2f} {stats['ROI']*100:>6.1f}")
    
    # 数据洞察 - Linus式直接判断
    print(f"\n=== 数据洞察与建议 ===")
    
    # 找异常值 - 用最简单的方法，不搞复杂统计
    print("1. 异常数据点检测:")
    if (df['CTR'] > df['CTR'].quantile(0.75) * 2).any():
        high_ctr = df[df['CTR'] > df['CTR'].quantile(0.75) * 2]['ad_id'].tolist()
        print(f"   - 异常高CTR广告: {high_ctr}")
    
    if (df['ROI'] < -0.5).any():
        severe_loss = df[df['ROI'] < -0.5]['ad_id'].tolist() 
        print(f"   - 严重亏损广告(ROI<-50%): {severe_loss}")
    
    # 活动表现排序
    campaign_roi = campaign_stats.sort_values('ROI', ascending=False)
    print(f"\n2. 活动表现排序(按ROI):")
    for i, (campaign, stats) in enumerate(campaign_roi.iterrows(), 1):
        status = "优秀" if stats['ROI'] > 1 else "一般" if stats['ROI'] > 0 else "亏损"
        print(f"   {i}. {campaign}: ROI {stats['ROI']*100:.1f}% ({status})")
    
    return df, worst_ads, campaign_stats

if __name__ == "__main__":
    # Linus说：Keep it simple, stupid
    csv_file = "/Users/zhangqingyue/Gaussian/test/learnagent/demo-data/sales-data.csv"
    
    print("广告数据分析报告")
    print("=" * 50)
    print("分析师: Linus式数据驱动方法")
    print("原则: 用数据说话，不搞理论，直接给结论\n")
    
    df, worst_ads, campaign_stats = analyze_ad_performance(csv_file)
    
    print(f"\n=== 终极结论和建议 ===")
    print("基于数据的硬核事实:")
    print(f"1. 最差广告是 {worst_ads.iloc[0]['ad_id']}，ROI仅{worst_ads.iloc[0]['ROI']*100:.1f}%")
    print(f"2. 最佳活动是 {campaign_stats.sort_values('ROI', ascending=False).index[0]}")
    print(f"3. 整体平均ROI: {df['ROI'].mean()*100:.1f}%")
    
    print(f"\n立即行动建议:")
    print(f"1. 停掉ROI<0的广告: {list(df[df['ROI'] < 0]['ad_id'])}")
    print(f"2. 增加投入到最佳广告: {list(df.nlargest(2, 'ROI')['ad_id'])}")
    print(f"3. 重点优化转化率<2%的广告")
    
    print(f"\n数据就是这样，不会撒谎。")
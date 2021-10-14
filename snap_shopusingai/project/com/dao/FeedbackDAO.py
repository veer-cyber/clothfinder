from snap_shopusingai.project import db
from snap_shopusingai.project.com.vo.FeedbackVO import FeedbackVO
from snap_shopusingai.project.com.vo.LoginVO import LoginVO


class FeedbackDAO:
    def insertFeedback(self, feedbackVO):
        db.session.add(feedbackVO)

        db.session.commit()

    def viewFeedback(self, feedbackVO):
        feedbackList = FeedbackVO.query.filter_by(feedbackFrom_LoginId=feedbackVO.feedbackFrom_LoginId).all()

        return feedbackList

    def adminviewFeedback(self):
        feedbackList = db.session.query(FeedbackVO, LoginVO).join(LoginVO,
                                                                  FeedbackVO.feedbackFrom_LoginId == LoginVO.loginId).all()

        return feedbackList

    def shopkeeperviewFeedback(self):
        feedbackList = db.session.query(FeedbackVO, LoginVO).join(LoginVO,
                                                                  FeedbackVO.feedbackFrom_LoginId == LoginVO.loginId).all()

        return feedbackList

    def deleteFeedback(self, feedbackId):
        feedbackList = FeedbackVO.query.get(feedbackId)

        db.session.delete(feedbackList)

        db.session.commit()

    def viewFeedbackReview(self, feedbackVO):
        db.session.merge(feedbackVO)

        db.session.commit()
